""" 
merge_image takes three parameters first two parameters specify 
the two images to be merged and third parameter i.e. vertically
is a boolean type which if True merges images vertically
and finally saves and returns the file_name
"""
from PIL import Image
import os
import numpy as np

def merge_image(img1, img2, vertically, outfile):
    images = list(map(Image.open, [img1, img2]))
    widths, heights = zip(*(i.size for i in images))
    if vertically:
        max_width = max(widths)
        total_height = sum(heights)
        new_im = Image.new('RGB', (max_width, total_height))

        y_offset = 0
        for im in images:
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]
    else:
        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]
    new_im.save(outfile)

def merge_folder(folder, block_size, width, height):

    # calculate how many blocks (see line 60) will occupy horizontal and vertical portion
    hor = int(width*block_size**(-1))
    ver = int(height*block_size**(-1))

    # load all the files in the current folder
    l = os.listdir(folder)
    L = []
    k = []
    # now if you are in some other directory, get to this directory because we
    # are going to merge images which would be easy if we come to this directory.
    cwd = os.getcwd()
    os.chdir(folder)

    # L stores all the .png files. eg. 1.png, 2.png, 3.png, ...
    for f in l:
        if f.endswith('.png'):
            L.append(f)

    counter = 1
    while counter != len(L)+1:
        k.append(str(counter)+'.png')
        counter += 1

    k = np.array(k)
    # reshape these n.png type images (blocks) into proper block dimensions.
    k = k.reshape((ver, hor))
    k = k.tolist()

    count = 1 # this keeps track of the rows k = [[1,2,3,...,8], [9,10,11,...,16], ...]
    #                                                count = 1     count = 2
    for h in k: # h takes row by row.
        i=0
        while i!=len(h):
            if i == 0:
                # if i==0, then join 1 and 2.
                merge_image(h[i], h[i+1], 0, 'test{}.png'.format(count))
                i+=2 # jump to 3 and save the cascase of 1 and 2 as test1.png.
            else:
                merge_image('test{}.png'.format(count), h[i], 0, 'test{}.png'.format(count))
                # concatenate test1.png and 3, save as again test1.png, concatenate 4, save as test1.png and so on.
                i+=1
            # thus test1.png is a cascade of 1,2,3,4,5,6,7,8.pngs.
            # update count by 1 and save as test2.png as cascade of 9,10,11,12,13,14,15,16.pngs.
        count+=1

    # again load all the files in this folder.
    l = os.listdir(folder)
    L= []
    h = []

    # this time load all those pngs which have 'test' in them.
    # That means we are loading all the cascades (horizontal cascades) and then load them to h.
    for i in l:
        if i.endswith('.png') and 'test' in i:
            L.append(i)
    
    counter = 1
    while counter != len(L)+1:
        h.append('test{}.png'.format(counter))
        counter += 1

    i = 0
    while i!=len(k): # len(k) or len(h) because h has horizontal cascades now and k is a 2d list containing
        # horizontal blocks.
        if i == 0:
                # join first 2 vertical blocks (blocks = horizontal cascades) and store in final{}.png
                merge_image(h[i], h[i+1], 1, 'final{}.png'.format(os.path.basename(folder)))
                i+=2
        else:
                merge_image('final{}.png'.format(os.path.basename(folder)), h[i], 1, 'final{}.png'.format(os.path.basename(folder)))
                # logic is same as above.
                i+=1
