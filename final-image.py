import encoder
import numpy as np
import imgConversion as img
import errorCorrection as decoder
import generateField
from tqdm import tqdm
import cv2

def main():
    n = 51
    k = 19
    field_n = 8
    t = 5
    beta = int((2**field_n - 1)/n)

    [GF, I_GF] = generateField.field(field_n)
    image = cv2.imread('testImageColor.png')
    cv2.imshow("img", image)
    msgBlock = []
    codewordBlock = []
    extBitCount = 0
    extCodeCount = 0

    info = list(img.encode(image))
    info = [int(i) for i in info]

    while len(info) % k != 0:
        info = info + [0]
        extBitCount += 1

    for i in range(0, len(info), k):
        msgBlock.append(info[i: i+k])

    print("Encoding")
    for m in tqdm(msgBlock):
        codewordBlock.append(encoder.encoder_51_19(m))

    while len(codewordBlock) % n != 0:
        codewordBlock.append([0 for _ in range(n)])
        extCodeCount += 1
    print("Codeword Block Ready")
    

    rcvMsg = ""
    ext = extBitCount + (extCodeCount * k)

    h = [[] for i in range(0, 2*t)]
    for i in range(0, 2*t):
        for j in range(0, n):
            h[i].append((beta * (i + 1) * j) % (2**field_n - 1))

    print("Decoding:")
    for i in tqdm(range(0, len(codewordBlock), n)):
        sentBlock = np.transpose(codewordBlock[i: i + n]).tolist()
        corrBlock = decoder.receiver(field_n, n, t, GF, I_GF, h, sentBlock)


        for i in range(len(corrBlock)):
            x = corrBlock[i][n - k: ]
            # print(x)
            rcvMsg = rcvMsg + "".join([str(num) for num in x])
        
    rcvMsg = rcvMsg[0: len(rcvMsg) - ext]
    image = img.decode(rcvMsg)
    cv2.imshow("img", image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()