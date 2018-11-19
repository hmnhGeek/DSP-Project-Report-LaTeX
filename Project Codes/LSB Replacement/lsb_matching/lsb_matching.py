# LSB Matching Algorithm

"""
    WARNING: Images that start with white color from (0, 0) should never be used.
    Because, lsb_embedding(255, 255, mi, mip1) ==> probable output having 256 as pixel
    value, which saturates to 255 in python. This makes us loose one bit of message.
    Hence white images are lossy, and they should not be used with this algorithm.
"""

# AUTHOR: Himanshu Sharma

from PIL import Image
import numpy as np
import scipy.misc

def bit_convert(n):
    '''
        Converts binary(n) to 8 bit.
        Retrun type: str
    '''
    val = str(bin(n))[2::]
    # add zeros to the beginning of val.
    # the no. of zeros = 8 - len(val).
    val = '0'*(8 - len(val)) + val

    return val

def LSB(n):
    '''
        Returns the LSB value of binary(n).
    '''
    return int(str(bin(n))[-1])

def binary_function(l, n):
    '''
        Returns the bivariate value of l and n
        binary_function(l,n) = LSB(floor(l/2) + n)
    '''
    # take the floor of l/2
    floor_value = l/2
    # Add this to n
    val = floor_value + n
    # convert this to binary and return the LSB
    return LSB(val)

def lsb_embedding(xi, xip1, mi, mip1):
    '''
        Implements mi and mip1 embedding in the consecutive pixels xi and xip1.
        Where mi and mip1 are the message message bits.

        Reference
        =========
        Please refer to the pdf document for the algorithm.
    '''
    if mi == LSB(xi):
        if mip1 != binary_function(xi, xip1):
            yip1 = xip1 + 1
        else:
            yip1 = xip1
        yi = xi
    else:
        if mip1 == binary_function(xi - 1, xip1):
            yi = xi - 1
        else:
            yi = xi + 1
        yip1 = xip1
    return yi, yip1

def message_bits(yi, yip1):
    '''
        Returns the two message bits from the modified pixel values.

        Again, refer to the document for the algorithm.
    '''
    return LSB(yi), binary_function(yi, yip1)

def image_embedding(cover, message, stego_image='out.png'):
    '''
        Returns the cover image with embedded message.
    '''

    # initialise a binary string.
    bstr = ''

    # iterate over each character and convert it into 8 bit binary number.
    for i in message:
        bstr += bit_convert(ord(i))

    # we now have the message information as multiple 8 bit blocks in bstr.
    # open the image now.
    img = Image.open(cover)
    pix = img.load()

    # load the dimensions of image.
    width, height = img.size
    lin_arr = []

    # convert the pixels to linear 1 D array.
    for row in range(height):
        for col in range(width):
            lin_arr.append(pix[col, row])

    # initialise an array to store modified pixels.
    mod_pix = []

    # check if message can be embedded or not. width*height = no of pixels.
    if width * height >= len(bstr):
        # message can be embedded.
        # now take group of 2 consecutive pixels.
        group = 2
        for i in range(0, len(lin_arr), group):
            block = lin_arr[i:i+group]
            
            # now we have 2 pixels.
            # we will operate on Blue channel only (r, g, b)
            xi = int(block[0][-1])
            xip1 = int(block[1][-1])

            # now take 2 blocks of bstr.
            bstr_block = bstr[i:i+group]
            
            try:
                mi = int(bstr_block[0])
                mip1 = int(bstr_block[1])

                yi, yip1 = lsb_embedding(xi, xip1, mi, mip1)

                # form the modified tuple.
                mod_pix.append((block[0][0], block[0][1], int(yi)))
                mod_pix.append((block[1][0], block[1][1], int(yip1)))
                
            except:
                mod_pix.append(block[0])
                mod_pix.append(block[1])

        # save a new image which is stego image.
        new_image = Image.new(img.mode, img.size)
        new_image.putdata(mod_pix)
        scipy.misc.imsave(stego_image, new_image)
        return "Key: {}".format(len(bstr))

def expose_message(stego_image, key):
    '''
        Returns the message stored in the stego-image.
    '''
    # open the image.
    img = Image.open(stego_image)
    pix = img.load()
    width, height = img.size

    # store the LSB bit in a string
    bstr = ''

    # initialise a message string.
    message = ''

    # initialise a linear array to store pixel values.
    lin_arr = []

    for row in range(height):
        for col in range(width):
            lin_arr.append(pix[col, row])

    # now take 2 pixels at a time and decode the message bits.
    for i in range(0, key, 2):
        pix1 = lin_arr[i]
        pix2 = lin_arr[i+1]

        # extract the blue channels of both the pixels.
        blue1 = pix1[-1]
        blue2 = pix2[-1]

        # get the message bits.
        mi, mip1 = message_bits(blue1, blue2)

        # store the mi and mip1 in bstr.
        bstr += str(mi) + str(mip1)

    # now we have a binary string of message whose length is a multiple of 8.
    # Why? because we made each character of msg bit an 8 bit binary number before
    # embedding it into stego-image.
    # Hence, iterate on each 8 block.
    for i in range(0, len(bstr), 8):
        current_block = bstr[i: i+8]
        # add '0b' to make it a pythonic binary string.
        current_block = '0b' + current_block
        # if we eval() current_block, it will give ord of a character.
        char_ord_value = eval(current_block)
        # get the character and store it in message string.
        message += chr(char_ord_value)

    # return the message
    return message

