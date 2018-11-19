from PIL import Image
import numpy as np
import os, random, shutil
import merge_images

'''
    AUTHOR: Himanshu Sharma
    Pixel Value Differencing based Steganography
    ============================================
'''

def split_blocks(image, block_size=5):
    # open the image
    i = Image.open(image)

    # find the dimensions of the image
    width, height = i.size
    # find the folder in which the image resides
    folder = os.path.dirname(image)
    # create an invisible directory in this folder to save the blocks.
    if not os.path.isdir(os.path.join(folder, '.'+str(os.path.basename(image).split('.')[0]))):
        os.mkdir(os.path.join(folder, '.'+str(os.path.basename(image).split('.')[0])))
        
    invisible = os.path.join(folder, '.'+str(os.path.basename(image).split('.')[0]))
    # note the current directory.
    curr_dir = os.getcwd()
    # change to the invisible directory.
    os.chdir(invisible)

    # before dividing the image into blocks, decide if it is even possible or not.
    # if the block size is less than or equal to the image dimension, then blocks could be
    # carved out. Eg. for 500 X 500 image, block size of 800 is meaningless unless you assign
    # the rule that if that is the case make block size to the maximum of the dimension, i.e.,
    # 500.
    if width >= block_size and height >= block_size:
        # find the new height and width of the image.
        # we are actually reshaping the image so that it could be divided into the blocks.
        # for example, if we have 21 X 13 image and a block size of 5, divide each subspace by 5,
        # i.e., 21/5 = 4.2. Take round => 4. Multiply by block size again => 4*5 = 20. Similarly, with
        # height, floor(13/5) = 3 ---> 3*5 = 15. So new image is 20 X 15 so that it could be divided into 5 X 5
        # blocks. The number of 5 X 5 blocks is now, 20*15/(5 X 5) = 12.
        new_width = np.round(width*(block_size**(-1)))*block_size
        new_height = np.round(height*(block_size**(-1)))*block_size
        # resize the image with the new dimensions.
        img = i.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        # load all the pixels of the image.
        pix = img.load()

        # calculate the number of blocks in vertical direction and horizontal direction.
        vertical_blocks = int(new_height/block_size)
        horizontal_blocks = int(new_width/block_size)
        counter =1

        for row in range(vertical_blocks):
            # iterate row wise on the horizontal block row.
            # vlow
            # +----------+
            # |          |
            # |          |
            # |          |  <========= A simple block or chunk of the whole image.
            # |          |
            # +----------+
            # vup
            vlow = row*block_size
            vup = (row+1)*block_size
            for col in range(horizontal_blocks):
                # once the row block is fixed, iterate over columns.
                # vlow/hlow hlow/hup  hup/hlow  hlow/hup  hlow/hup    hup
                # +----------+----------+----------+----------+----------+
                # |          |          |          |          |          |
                # |          |          |          |          |          |
                # |          |          |          |          |          |
                # |          |          |          |          |          |
                # +----------+----------+----------+----------+----------+
                # vup
                hlow = col*block_size
                hup = (col+1)*block_size
                # crop this chunk.
                image_block = img.crop((hlow, vlow, hup, vup))
                # save this chunk in the same directory
                image_block.save(str(counter)+'.png')
                # increase the counter by 1.
                counter += 1
        print("You must expect "+str(new_width*new_height/(block_size**2))+" photos.")
        os.chdir(curr_dir)
        return new_width, new_height, width, height, invisible

def random_angle_rotations(image_block):
    '''
        Takes an image block and rotate it with a random angle.
    '''
    random_angles_degrees = np.array([0, 90, 180, 270])
    random_angles_radians = (np.pi/180.0)*random_angles_degrees

    # choose a random angle.
    angle = random.choice(random_angles_degrees)
    
    # open the image.
    img = Image.open(image_block).convert('RGBA')
    # rotate the image by random angle generated above.
    img = img.rotate(angle)
    img.save(image_block)

    return angle

def raster_scan(folder, width, height):
    '''
        Takes in a folder and then joins all the blocks to form an image of width X height.
    '''
    # store all the blocks in a list.
    blocks = os.listdir(folder)

    # take a block from this list.
    blk = blocks[0]

    # store the current directory.
    curr_dir = os.getcwd()
    # change to the folder directory.
    os.chdir(folder)

    # find the dimension of a block.
    blk_image = Image.open(blk)
    w, h = blk_image.size

    # initialise a counter.
    counter = 1
    max_length = len(blocks)

    # check if the block is a square or not.
    if w != h:
        print("Got 0 because block is not a square.")
        return 0
    else:
        # divide width into blocks number.
        horizontal_units = width*w**(-1)
        # divide height into blocks number.
        vertical_units = height*h**(-1)

        # make an empty list which will store the rowwise blocks.
        rows = []

        # check if the number of blocks is equal to vertical_units X horizontal_units.
        if vertical_units*horizontal_units == max_length:
            # iterate over vertical units.
            for row in range(int(vertical_units)):
                # take the first block
                first = row*int(horizontal_units) + 1
                first_block = Image.open(str(first)+'.png')
                # now iterate over columns, but from second block.
                xoffset = 0
                for col in range(first+1, first+int(horizontal_units)):
                    # take the block under consideration.
                    current_block = Image.open(str(col)+'.png')
                    first_block.paste(current_block, (xoffset, 0))
                    # add width of block as offset in horizontal direction.
                    xoffset += w#current_block.size[0]
                first_block.save('first'+str(row)+'.png')
                rows.append(first_block)
            # code for vertical concatination begins here.
            # first strip
            first_strip = rows[0]
            yoffset = 0
            for i in range(1, len(rows)):
                print(i)
                first_strip.paste(rows[i], (0, w))
                yoffset += rows[i].size[1]
            # save the first_strip
            first_strip.save('final.png')
            os.chdir(curr_dir)
            return rows
        else:
            print("Another reason")
            return 0

def raster_scan(image_array):
    """
        Basically reshapes any image into 1 X mn.
    """
    image_array = image_array.convert('L')
    image_array = np.reshape(image_array, (1, -1))[0]
    return image_array

def step1(image, block_size=5, dont_delete=False):
    # call the split_blocks function to split image into blocks.
    print("Splitting image")
    new_width, new_height, width, height, invisible_dir = split_blocks(image, block_size)
    
    # change to the invisible directory.
    cwd = os.getcwd()
    os.chdir(invisible_dir)

    # find all the images.
    l = os.listdir(os.getcwd())
    # arrange them in increasing order.
    k = []
    counter = 1
    while counter != len(l)+1:
        k.append(str(counter)+'.png')
        counter += 1

    # now k contains all the images in increasing order.
    # radomly rotate them.
    angles = []
    print("Rotating blocks")
    for i in k:
        angles.append(random_angle_rotations(i))

    # now merge the rotated images.
    print("Joining rotated blocks")
    merge_images.merge_folder(os.getcwd(), block_size, new_width, new_height)

    # find the main directory.
    mainDir = os.path.dirname(image)

    # get image name only, without extension
    image_name = os.path.basename(image).split('.')[0]

    # move the generated image to mainDir.
    tempfolder = os.getcwd()
    os.rename(os.path.join(tempfolder, 'final.'+image_name+'.png'), os.path.join(mainDir, 'final.'+image_name+'.png'))

    # temporary folder is of no use now. Delete it!
    os.chdir(cwd)
    if not dont_delete:
        shutil.rmtree(tempfolder)

    # raster scan the scrumbled image which is stored in the mainDir.
    os.chdir(mainDir)
    # open the scrumbled image. raster_scan() internally converts to grayscale.
    scrumbled_image = Image.open('final.'+image_name+'.png')
    scrumbled_image = raster_scan(scrumbled_image)

    # iterate in consecutive_difference to find the pixels variations greater than threshold parameter 't'.
    t = 15

    # group the pixels in the pair of 2.
    new_image = list(zip(scrumbled_image[::2],scrumbled_image[1::2]))
    new_image = np.array(new_image)

    # select those pairs where difference is greater than 't'.
    EU = new_image[np.abs(new_image[:,0].astype(int) - new_image[:,1].astype(int)) >= t]
    print(EU)
    
    return angles
