import encoder
import numpy as np
import errorCorrection as decoder
import generateField
import random
import time

def main():
    start_time = time.time()
    n = 31
    k = 11
    field_n = 5
    t = 5
    beta = int((2**field_n - 1)/n)
    f = open("testText.txt", "r")
    msg = f.readline()
    f.close()
    print("Message:\n", msg)
    print("Total Number of Characters: ", len(msg))
    info = []
    msgBlock = []
    codewordBlock = []

    [GF, I_GF] = generateField.field(field_n)
    for i in range(0, len(msg)):
        x = list(bin(ord(msg[i]))[2:])
        # print(x, msg[i])
        while len(x) < 7:
            x = ['0'] + x
        info = info + [int(s) for s in x]
    
    while len(info) % k != 0:
        info = info + [0]

    
    for i in range(0, len(info), k):
        msgBlock.append(info[i: i+k])
 
    for m in msgBlock:
        codewordBlock.append(encoder.encoder_31_11(m))

    while len(codewordBlock) % n != 0:
        codewordBlock.append([0 for _ in range(n)])

    h = [[] for i in range(0, 2*t)]
    for i in range(0, 2*t):
        for j in range(0, n):
            h[i].append((beta * (i + 1) * j) % (2**field_n - 1))
    # print(h)

    print("Total Number of Encoded Blocks: ", int(len(codewordBlock)/n))
    print("Encoding Type: ", n, k)
    rcvMsg = []

    for i in range(0, len(codewordBlock), n):
        sentBlock = np.transpose(codewordBlock[i: i + n]).tolist()
        corrBlock = decoder.receiver(field_n, n, t, GF, I_GF, h, sentBlock)
        
        for j in range(len(corrBlock)):
            rcvMsg = rcvMsg + corrBlock[j][n - k: ]

    msgStr = ""
    zeros = [0 for _ in range(7)]
    for j in range(0, len(rcvMsg), 7):
        x = rcvMsg[j: j + 7]
        if x == zeros:
            break
        x = [str(m) for m in x]
        msgStr = msgStr + chr(int("".join(x), 2))
    print("\nMessage Received:\n", msgStr)
    print("Execution Time: ", time.time() - start_time, "s")
            

if __name__ == "__main__":
    main()
