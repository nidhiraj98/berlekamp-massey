import encoder
import numpy as np
import imgConversionSrinag as img
import errorCorrection as decoder
import generateField
from tqdm import tqdm
import cv2

def main():
    n = 31
    k = 11
    field_n = 5
    t = 5

    GF = generateField.field(field_n)
    image = cv2.imread('image.png')
    # info = []
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

    print("Msg Block Ready")
    print("Encoding")
    for m in tqdm(msgBlock):
        codewordBlock.append(encoder.encoder_31_11(m))

    while len(codewordBlock) % n != 0:
        codewordBlock.append([0 for _ in range(n)])
        extCodeCount += 1
    print("Codeword Block Ready")
    

    rcvMsg = ""
    ext = extBitCount + (extCodeCount * k)

    print("Decoding:")
    for i in tqdm(range(0, len(codewordBlock), n)):
        sentBlock = np.transpose(codewordBlock[i: i + n]).tolist()
        corrBlock = decoder.receiver(field_n, t, GF, sentBlock)


        for i in range(len(corrBlock)):
            x = corrBlock[i][n - k: ]
            # print(x)
            rcvMsg = rcvMsg + "".join([str(num) for num in x])
        
    rcvMsg = rcvMsg[0: len(rcvMsg) - ext]

    for i in range(len(rcvMsg)):
        if rcvMsg[i] != str(info[i]):
            print(i)
            break
    image = img.decode(rcvMsg)
    cv2.imshow("img", image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()