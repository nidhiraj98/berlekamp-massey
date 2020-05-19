import encoder
import numpy as np
import errorCorrection as decoder

def main():
    n = 31
    k = 11
    field_n = 5
    t = 5
    msg = input("Enter Message:")
    info = []
    msgBlock = []
    codewordBlock = []
    extCount = 0

    for i in range(0, len(msg)):
        x = list(bin(ord(msg[i]))[2:])
        while len(x) < 7:
            x = [0] + x
        info = info + [int(s) for s in x]
    
    while len(info) % k != 0:
        info = info + [0]
    
    while len(info) >= k:
        msgBlock.append(info[0: k])
        info = info[k:len(info)]

    for m in msgBlock:
        codewordBlock.append(encoder.encoder_31_11(m))

    while len(codewordBlock) % n != 0:
        extCount += 1
        codewordBlock.append([0 for _ in range(n)])
        
    blockCount = int(len(codewordBlock) / n)

    for i in range(blockCount):
        sentBlock = np.transpose(codewordBlock[0: n]).tolist()
        corrBlock = decoder.receiver(field_n, t, sentBlock)
        if len(codewordBlock) > n:
            codewordBlock = codewordBlock[n + 1: ]

        
        rcvMsg = []
        for i in range(len(corrBlock) - extCount):
            rcvMsg = rcvMsg + corrBlock[i][n - k: ]
        

        msgStr = ""
        zeros = [0 for _ in range(7)]
        charCount = int(len(rcvMsg)/ 7)
        for i in range(charCount + 1):
            x = rcvMsg[0: 7]
            if x == zeros:
                break
            x = [str(m) for m in x]
            msgStr = msgStr + chr(int("".join(x), 2))
            rcvMsg = rcvMsg[7: ]
        print(msgStr)
            

if __name__ == "__main__":
    main()