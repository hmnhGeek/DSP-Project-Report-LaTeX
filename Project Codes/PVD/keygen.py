import numpy as np
def generate_key(data_list):
    # converts a list of integers into list of string.
    string = [str(i) for i in data_list]
    dummy = []

    # since the possible angles are in atmost 3 digits add zeros in front
    for i in string:
        dummy.append(i)
    
    L = [chr(int(i)) for i in dummy]
    l = ' '.join(L)
    return l

def generate_angles(key):
    l = key.split(' ')
    L = [ord(i) for i in l]
    return L
