import encoder
import errorCorrection
import generateField
import random
import math
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def genErrRate(pT, samples):
    n = 31
    k = 11
    field_n = 5
    t = 5
    GF = generateField.field(field_n)

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
        print("Power = ", power)
        error = 0
        for sample in tqdm(range(1, samples)):
            msg = [random.randrange(2) for _ in range(k)]
            codeword = encoder.encoder_31_11(msg)
            # print(codeword)
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
            # print(codewordChannel)
            decoded = errorCorrection.berlekamp(field_n, n, t, GF, codewordChannel)
            # print(decoded)
            msgEst = decoded[n - k: ]
            # print(msgEst)
            errPat = np.bitwise_xor(msg, msgEst)
            error += sum(errPat)
            # print(error)
        errRate.append(error / (k * sample))
    return errRate
# rate  = genErrRate(range(-30, 20), 1000)
# plt.semilogy(range(-30, 20), rate)
# plt.show()