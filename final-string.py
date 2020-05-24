import encoder
import numpy as np
import errorCorrection as decoder
import generateField
import random

def main():
    n = 51
    k = 27
    field_n = 8
    t = 5
    beta = int((2**field_n - 1)/n)
    msg = input("Enter Message:")
    info = []
    msgBlock = []
    codewordBlock = []

    [GF, I_GF] = generateField.field(field_n)
    for i in range(0, len(msg)):
        x = list(bin(ord(msg[i]))[2:])
        while len(x) < 7:
            x = ['0'] + x
        info = info + [int(s) for s in x]
    
    while len(info) % k != 0:
        info = info + [0]

    
    for i in range(0, len(info), k):
        msgBlock.append(info[i: i+k])
 
    for m in msgBlock:
        codewordBlock.append(encoder.encoder_51_27(m))

    while len(codewordBlock) % n != 0:
        codewordBlock.append([0 for _ in range(n)])
        
    blockCount = int(len(codewordBlock) / n)


    h = [[] for i in range(0, 2*t)]
    for i in range(0, 2*t):
        for j in range(0, n):
            h[i].append((beta * (i + 1) * j) % (2**field_n - 1))
    # print(h)


    for i in range(blockCount):
        sentBlock = np.transpose(codewordBlock[0: n]).tolist()
        corrBlock = decoder.receiver(field_n, n, t, GF, I_GF, h, sentBlock)
        
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