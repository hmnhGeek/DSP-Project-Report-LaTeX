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

    hor = int(width*block_size**(-1))
    ver = int(height*block_size**(-1))
    
    l = os.listdir(folder)
    L = []
    k = []
    cwd = os.getcwd()
    os.chdir(folder)
    
    for f in l:
        if f.endswith('.png'):
            L.append(f)

    counter = 1
    while counter != len(L)+1:
        k.append(str(counter)+'.png')
        counter += 1

    k = np.array(k)
    k = k.reshape((ver, hor))
    k = k.tolist()

    count = 1
    for h in k:
        i=0
        while i!=len(h):
            if i == 0:
                merge_image(h[i], h[i+1], 0, 'test{}.png'.format(count))
                i+=2
            else:
                merge_image('test{}.png'.format(count), h[i], 0, 'test{}.png'.format(count))

                i+=1
        count+=1

    l = os.listdir(folder)
    L= []
    h = []
    
    for i in l:
        if i.endswith('.png') and 'test' in i:
            L.append(i)
    
    counter = 1
    while counter != len(L)+1:
        h.append('test{}.png'.format(counter))
        counter += 1

    i = 0
    while i!=len(k):
        if i == 0:
                merge_image(h[i], h[i+1], 1, 'final{}.png'.format(os.path.basename(folder)))
                i+=2
        else:
                merge_image('final{}.png'.format(os.path.basename(folder)), h[i], 1, 'final{}.png'.format(os.path.basename(folder)))

                i+=1
