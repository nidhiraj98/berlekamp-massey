import cv2
import numpy as np
from functools import reduce


def int_to_bin(int_arr):
    return ''.join(map(lambda byte: format(byte, '08b'), int_arr))


def bin_to_int(bin_str):
    return [int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8)]


def encode(img):
    sep = '|'
    shape = img.shape
    n_bytes = reduce(lambda r, x: r*x, shape)
    str_shape = ','.join(str(dim) for dim in shape)

    bin_str_shape = int_to_bin(ord(ch) for ch in str_shape)
    bin_str_sep = int_to_bin([ord(sep)])
    bin_str_img = int_to_bin(img.reshape((n_bytes, )))

    return bin_str_shape + bin_str_sep + bin_str_img


def decode(data):
    sep = '|'
    data = bin_to_int(data)
    sep_i = data.index(ord(sep))
    str_shape = ''.join(chr(ch) for ch in data[:sep_i])

    shape = tuple(int(dim) for dim in str_shape.split(','))
    img = np.reshape(np.array(data[sep_i+1:], dtype=np.uint8), shape)

    return img
