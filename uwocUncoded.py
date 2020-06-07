import encoder
import errorCorrection
import generateField
import random
import math
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def genErrRate(pT, samples):
    k = 19

    rB = 500 * (10**6)
    tB = 1 / rB
    kB = 1.38 * (10 ** (-23))
    rL = 100
    tE = 256
    b = 2 * rB
    sigma = math.sqrt(4 * kB * tE * b/ rL)
    const = [0, 1]
    sigmaX = math.sqrt(0.165)
    muX = -(sigmaX **  2)
    eta = 0.15
    errRate = []

    for power in pT:
        # print("Encoding Type: ", n, k)
        print("Power: ", power)
        error = 0
        for sample in tqdm(range(1, samples)):
            msg = [random.randrange(2) for _ in range(k)]
            # print("Message vector:                  ", msg)
            codeword = msg
            # print("Codeword generated:              ", codeword)
            codewordChannel = []
            for code in codeword:
                r = random.gauss(muX, sigmaX)
                hsr = math.exp(2 * r)
                esr = random.gauss(0, 1)
                ysr = eta * hsr * math.sqrt(10 **(power * 0.1) * tB) * code + sigma * esr
                dec = 10 ** 90
                for i in range(2):
                    dis  = (ysr - eta * hsr * math.sqrt(10 ** (power * 0.1) * tB) * const[i]) ** 2
                    if dis < dec:
                        dec = dis
                        x1 = const[i]
                codewordChannel.append(x1)
            # print("Received vector after channel:   ",codewordChannel)
            # print("Codeword after error correction: ",decoded)
            msgEst = codewordChannel
            # print("Decoded Message:                 ",msgEst)
            errPat = np.bitwise_xor(msg, msgEst)
            error += sum(errPat)
        errRate.append(error / (k * sample))
    return errRate

# genErrRate(range(-30, 20), 10**4)
# print(genErrRate(range(0, 1), 10**2))
# rate  = genErrRate(range(-30, 20), 10**4)
# plt.semilogy(range(-30, 20), rate)
# plt.show()