import encoder
import numpy as np
import errorCorrection as decoder
import generateField

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

    GF = generateField.field(field_n)
    for i in range(0, len(msg)):
        x = list(bin(ord(msg[i]))[2:])
        while len(x) < 7:
            x = [0] + x
        info = info + [int(s) for s in x]
    
    while len(info) % k != 0:
        info = info + [0]
    
    for i in range(0, len(info), k):
        msgBlock.append(info[i: i+k])

    for m in msgBlock:
        codewordBlock.append(encoder.encoder_31_11(m))

    while len(codewordBlock) % n != 0:
        extCount += 1
        codewordBlock.append([0 for _ in range(n)])
        
    blockCount = int(len(codewordBlock) / n)

    for i in range(blockCount):
        sentBlock = np.transpose(codewordBlock[0: n]).tolist()
        corrBlock = decoder.receiver(field_n, t, GF,sentBlock)

        
        rcvMsg = []
        for i in range(len(corrBlock)):
            rcvMsg = rcvMsg + corrBlock[i][n - k: ]
        

        msgStr = ""
        zeros = [0 for _ in range(7)]
        charCount = int(len(rcvMsg)/ 7)
        for i in range(0, charCount + 1, 7):
            x = rcvMsg[i: i + 7]
            if x == zeros:
                break
            x = [str(m) for m in x]
            msgStr = msgStr + chr(int("".join(x), 2))
        print(msgStr)
            

if __name__ == "__main__":
    main()