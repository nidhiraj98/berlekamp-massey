import encoder
import numpy as np
import errorCorrectionPrimitive as decoder
import generateField
import random

def main():
    n = 51
    k = 19
    field_n = 8
    t = 5
    # print(a)
    msg = input("Enter Message:")
    info = []
    msgBlock = []
    codewordBlock = []

    GF = generateField.field(field_n)
    for i in range(0, len(msg)):
        x = list(bin(ord(msg[i]))[2:])
        while len(x) < 7:
            x = ['0'] + x
        info = info + [int(s) for s in x]
    
    while len(info) % k != 0:
        info = info + [0]
    # info = [random.randrange(2) for _ in range(k)]
    # print(info)
    
    for i in range(0, len(info), k):
        msgBlock.append(info[i: i+k])
 
    for m in msgBlock:
        codewordBlock.append(encoder.encoder_51_19(m))
    # print(codewordBlock)

    while len(codewordBlock) % n != 0:
        codewordBlock.append([0 for _ in range(n)])
        
    blockCount = int(len(codewordBlock) / n)

    for i in range(blockCount):
        sentBlock = np.transpose(codewordBlock[0: n]).tolist()
        corrBlock = decoder.receiver(field_n, n, t, GF,sentBlock)
        # print(corrBlock[0])
        
        rcvMsg = []
        for i in range(len(corrBlock)):
            rcvMsg = rcvMsg + corrBlock[i][n - k: ]

        msgStr = ""
        zeros = [0 for _ in range(7)]
        for i in range(0, len(rcvMsg), 7):
            x = rcvMsg[i: i + 7]
            if x == zeros:
                break
            x = [str(m) for m in x]
            msgStr = msgStr + chr(int("".join(x), 2))
        print(msgStr)
            

if __name__ == "__main__":
    main()