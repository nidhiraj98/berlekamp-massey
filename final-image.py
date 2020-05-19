import encoder
import numpy as np
import imgConversion as img
import errorCorrection as decoder
import generateField
from tqdm import tqdm

def main():
    n = 31
    k = 11
    field_n = 5
    t = 5

    GF = generateField.field(field_n)
    # msg = input("Enter Message:")
    image = img.load_img('image.png')
    # info = []
    msgBlock = []
    codewordBlock = []
    extCount = 0

    info = list(img.encode_img(image))
    info = [int(i) for i in info]
    # print(info)
    print("Image converted")
    
    while len(info) % k != 0:
        info = info + [0]
    
    # print("Zeros appended")
    # print("No. of message blocks = ", len(info) / k)
    for i in range(0, len(info), k):
        msgBlock.append(info[i: i+k])

    print("Msg Block Ready")
    print("Encoding")
    for m in tqdm(msgBlock):
        codewordBlock.append(encoder.encoder_31_11(m))

    while len(codewordBlock) % n != 0:
        extCount += 1
        codewordBlock.append([0 for _ in range(n)])
    print("Codeword Block Ready")
    

    blockCount = int(len(codewordBlock) / n)
    # print(blockCount)
    rcvMsg = []

    for _ in tqdm(range(blockCount)):
        sentBlock = np.transpose(codewordBlock[0: n]).tolist()
        corrBlock = decoder.receiver(field_n, t, GF, sentBlock)
        
        for i in range(len(corrBlock)):
            rcvMsg = rcvMsg + corrBlock[i][n - k: ]
        

        # msgStr = ""
        # zeros = [0 for _ in range(7)]
        # charCount = int(len(rcvMsg)/ 7)
        # for i in range(charCount + 1):
        #     x = rcvMsg[0: 7]
        #     if x == zeros:
        #         break
        #     x = [str(m) for m in x]
        #     msgStr = msgStr + chr(int("".join(x), 2))
        #     rcvMsg = rcvMsg[7: ]
        # print(msgStr)
        # codewordBlock = codewordBlock[n: ]
    print(rcvMsg)
    if rcvMsg == info:
        print("Correct")

if __name__ == "__main__":
    main()