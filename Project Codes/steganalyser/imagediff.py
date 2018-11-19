from PIL import Image

'''
    AUTHOR: Himanshu Sharma

    DESCRIPTION
    ===========
    Takes in two images as input and evaluates the differences between them.
'''

def bruteforce(image1, image2):
    # open the two images.
    i1 = Image.open(image1)
    i2 = Image.open(image2)
    # assertion made to check if the images have same modes. If
    # different, raise an AssertionError.
    assert i1.mode == i2.mode, "Different kinds of images."

    # pair up the index wise pixel values of the two images.
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale images, simple difference in the pixel
        # values is enough. Take the difference with its absolute and
        # store it in dif.
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        # else, if len is say 3, as is the case with RGB, then do this.
        # so if, p1 = (10, 20, 30) and p2 = (90, 100, 200), then zip(p1, p2)
        # is [(10, 90), (20, 100), (30, 200)] and the difference is taken and
        # then appended to dif.
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
     
    ncomponents = i1.size[0] * i1.size[1] * 3 # calculate the total number of pixel values present
    print("Difference (percentage):", (dif / 255.0 * 100) / ncomponents) # get the average percentage
