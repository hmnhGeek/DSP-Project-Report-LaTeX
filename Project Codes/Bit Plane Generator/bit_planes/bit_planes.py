from PIL import Image
import numpy as np
import scipy.misc

"""
    AUTHOR: Himanshu Sharma
    TITLE: Bit Plane Generator
    ==========================
"""

def generateGray(bit):
    '''
        Returns white or black value depending on the bit plane.
    '''
    bit = str(bit)
    if bit == '1':
        return 255
    else:
        return 0

def bitplane(binary, plane_no):
    '''
        Returns the plane_no th bit plane from the binary pixel.
    '''
    # convert the binary no to string, to avoid errors.
    binary = str(binary)

    # extract the plane_no-1 th bit from the binary.
    binary = binary[plane_no-1]
    return binary

def binary_generate(decimal_number):
    '''
        Returns the binary equivalent of the number in 8 bits.
    '''
    bits = 8
    # initialise a 'rem' array to store remainders from 2's divisions.
    rem = []
    while decimal_number != 0:
        rem.append(str(decimal_number%2))
        decimal_number /= 2
        
    binary = ''.join(rem[-1:-len(rem)-1:-1])
    # if it is less than 8 bits add zeros to front.
    while len(binary) < bits:
        binary = '0' + binary

    return binary

def string_to_integer(string):
    return int(string)

def generateBitPlane(image, plane_no=1):
    '''
        Returns the plane_no th bit plane of any image.
        Plane no 1 refers to the MSB and the last plane is of LSB.
    '''

    # open the image as grayscale.
    img = Image.open(image).convert('L')
    # convert image into numpy array for faster processing.
    arr_image = np.array(img)

    # vectorize binary_generate function to enable it operate on numpy arrays.
    numpy_binary = np.vectorize(binary_generate)
    # do similar thing with bitplane() function.
    numpy_bitplane = np.vectorize(bitplane)

    # use the new vectorized numpy_binary() to get the binary equivalent of all
    # the numpy array elements in 8 bits.
    arr_image = numpy_binary(arr_image)

    # now use the new vectorized numpy_bitplane() to get the bit plane of the elements
    # of the the numpy array.
    arr_image = numpy_bitplane(arr_image, plane_no)

    # vectorize string_to_integer() function
    numpy_str_to_int = np.vectorize(string_to_integer)

    # use this function now to get integer form of the bit plane.
    arr_image = numpy_str_to_int(arr_image)

    # multiply arr_image by 255 to get bit plane image array. So, at 1, we get 255 and at 0 its 0.
    arr_image = 255*arr_image

    # save this array as image
    scipy.misc.imsave(image+'bitplane{}.png'.format(plane_no), arr_image)

            
