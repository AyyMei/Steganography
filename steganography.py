import cv2
import numpy

# Bit masks
bitlist1 = [0b10000000, 0b11000000, 0b11100000, 0b11110000, 0b11111000, 0b11111100, 0b11111110, 0b11111111]
bitlist2 = [0b00000001, 0b00000011, 0b00000111, 0b00001111, 0b00011111, 0b00111111, 0b01111111, 0b11111111]

# Encode [img2] into [img1] as output [output]
# Takes the [bits] most significant bits of [img2] and places them into the [bits] least significant bits of [img1]
# [img1] and [img2] must have the same dimensions
def encode(img1, img2, bits, output):
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)

    h1 = img1.shape[0]
    w1 = img1.shape[1]
    h2 = img2.shape[0]
    w2 = img2.shape[1]
    out = numpy.zeros((h1,w1,3), numpy.uint8)

    if (h1 == h2 and w1 == w2):
        for i in range(w1):
            for j in range(h1):
                out.itemset((j,i,0), ((img1.item(j,i,0) >> bits) << bits) | ((img2.item(j,i,0) & bitlist1[bits-1]) >> 8 - bits))
                out.itemset((j,i,1), ((img1.item(j,i,1) >> bits) << bits) | ((img2.item(j,i,1) & bitlist1[bits-1]) >> 8 - bits))
                out.itemset((j,i,2), ((img1.item(j,i,2) >> bits) << bits) | ((img2.item(j,i,2) & bitlist1[bits-1]) >> 8 - bits))
    cv2.imwrite(output, out)

# Removes a possible hidden image from [img] as output [output]
# Takes the [bits] least significant bits of [img] and shifts them to the most significant bits out [output]
def decode(img, bits, output):
    img = cv2.imread(img)

    h = img.shape[0]
    w = img.shape[1]
    out = numpy.zeros((h,w,3), numpy.uint8)

    for i in range(w):
        for j in range(h):
            out.itemset((j,i,0), (img.item(j,i,0) & bitlist2[bits-1]) << 8 - bits)
            out.itemset((j,i,1), (img.item(j,i,1) & bitlist2[bits-1]) << 8 - bits)
            out.itemset((j,i,2), (img.item(j,i,2) & bitlist2[bits-1]) << 8 - bits)
    cv2.imwrite(output, out)