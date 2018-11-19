from PIL import Image
import numpy as np
import os, random, shutil
import merge_images
import pickle
import lsb_matching

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

def raster_scan(image_array):
    """
        Basically reshapes any image into 1 X mn.
    """
    image_array = image_array.convert('L')
    image_array = np.reshape(image_array, (1, -1))[0]
    return image_array

def generateMessage(message):
    string = ''
    for m in message:
        m = bin(ord(m))
        m = m[2::]
        m = m[-1:-len(m)-1:-1]
        while len(m) != 8:
            m = m +'0'
        m = m[-1:-len(m)-1:-1]
        string += m
    return string

def pixelate(image, message, block_size=5, dont_delete=False):

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
    scrumbled_image_name = 'final.'+image_name+'.png'

    # start the procedure of LSB Replacement
    key = lsb_matching.image_embedding(scrumbled_image_name, message, 'final.'+image_name+'-stego.png')
    print(key)

    # ----------------------------------------------------------------------------------------------------#
    # divide the stego image into same block size again
    new_width, new_height, width, height, new_inv_dir = split_blocks('final.'+image_name+'-stego.png', block_size)
    rev_angles = (-1*np.array(angles)).tolist()

    # change to the invisible directory.
    cwd = os.getcwd()
    os.chdir(new_inv_dir)

    # find all the images.
    l = os.listdir(os.getcwd())
    # arrange them in increasing order.
    k = []
    counter = 1
    while counter != len(l)+1:
        k.append(str(counter)+'.png')
        counter += 1

    for block in range(len(k)):
        # open the image = k[block]
        I = Image.open(k[block]).convert('RGBA')
        # rotate the image by reverse angle generated above.
        I = I.rotate(rev_angles[block])
        I.save(k[block])

    merge_images.merge_folder(os.getcwd(), block_size, new_width, new_height)

    # get image name only, without extension
    image_name = os.path.basename(image).split('.')[0]

    # move the generated image to mainDir.
    tempfolder = os.getcwd()
    os.rename(os.path.join(tempfolder, 'final.final.png'), os.path.join(mainDir, 'final.final.png'))

    # temporary folder is of no use now. Delete it!
    os.chdir(cwd)
    if not dont_delete:
        shutil.rmtree(tempfolder)

    # ----------------------------------------------------------------------------------------------------- #
    tup = angles, block_size, key, rev_angles
    # save this tuple in a file.
    f = open(scrumbled_image_name+'.dat', 'wb')
    pickle.dump(tup, f)
    f.close()

    os.chdir(cwd)
    os.remove('final.'+image_name+'.png')
    os.remove('final.'+image_name+'-stego.png')
    
    return 1


def decode(stego_image, key_file):
    """
        Decodes the stego image based on valid key_file.
    """

    f = open(key_file, 'rb')
    tup = pickle.load(f)
    f.close()

    angles, block_size, key, rev_angles = tup
    # divide the stego image into same block size again
    new_width, new_height, width, height, new_inv_dir = split_blocks(stego_image, block_size)

    # change to the invisible directory.
    cwd = os.getcwd()
    os.chdir(new_inv_dir)

    # find all the images.
    l = os.listdir(os.getcwd())
    # arrange them in increasing order.
    k = []
    counter = 1
    while counter != len(l)+1:
        k.append(str(counter)+'.png')
        counter += 1
        
    for block in range(len(k)):
        # open the image = k[block]
        I = Image.open(k[block]).convert('RGBA')
        # rotate the image by reverse angle generated above.
        I = I.rotate(angles[block])
        I.save(k[block])

    merge_images.merge_folder(os.getcwd(), block_size, new_width, new_height)

    # apply lsb_matching expose method.
    print('Decoding initiated...')
    key = key.split(' ')[1]
    msg = lsb_matching.expose_message('final.final.png', int(key))

    # remove .final folder. Of no use.
    tempfolder = os.getcwd()
    os.chdir(cwd)
    shutil.rmtree(tempfolder)
    return msg
