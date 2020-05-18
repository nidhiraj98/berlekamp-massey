import encoder
import numpy as np

def main():
    n = 31
    k = 11
    msg = input("Enter Message:")
    info = []
    msgBlock = []
    codewordBlock = []

    for i in range(0, len(msg)):
        i = list(bin(ord(msg[i]))[2:])
        info = info + [int(s) for s in i]
    
    while len(info) % k == 0:
        info = info + [0]

    while len(info) >= k:
        msgBlock.append(info[0: k])
        info = info[k:len(info)]

    for msg in msgBlock:
        codewordBlock.append(encoder.encoder_31_11(msg))

    while len(codewordBlock) % n != 0:
        codewordBlock.append([0 for _ in range(n)])
        
    blockCount = int(len(codewordBlock) / n)

    for i in range(blockCount):
        print(np.transpose(codewordBlock[0: n]).tolist())
        if len(codewordBlock) > n:
            codewordBlock = codewordBlock[n + 1: ]


if __name__ == "__main__":
    main()