import numpy as np

class LSBEncoder():
    def __init__(self):
        pass
    

    def binaryConvert(self, character):
        # ordinate of the character.
        ordinate = ord(character)
        # binary equivalent of the ordinate.
        binary = bin(ordinate)

        return binary[2::]

    def f(a, b):
        return self.LSB(np.floor(a/2) + b)

    def LSB(self, xi):
        binary = bin(xi)
        return binary[-1]

    def encode_pixel_pair(self, xi, xip1, mi, mip1):
        r = 1
        if self.LSB(xi) == mi and self.f(xi, xip1) == mip1:
            return (xi, xip1)
        elif self.LSB(xi) == mi and self.f(xi, xip1) != mip1:
            return (xi, xip1 + r)
        elif self.LSB(xi) != mi and self.f(xi-1, xip1) == mip1:
            return (xi -1, xip1)
        elif self.LSB(xi) != mi and self.f(xi-1, xip1) != mip1:
            return (xi+1, xip1)

    def readjust(self, xi, xip1, T):
        # use this when either xi and xip1 are not in range [0, 255] or when
        # xip1 - xi < T.
        if np.abs(xip1 - xi) < T or (xip1 not in range(0, 256) or xi not in range(0, 256)):
            pass
        else:
            return 0
            
