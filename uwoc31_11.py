import encoder
from galoisField import generateField
import errorCorrection
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
    beta = int((2**field_n - 1)/n)
    [GF, I_GF] = generateField.field(field_n)

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

    h = [[] for i in range(0, 2*t)]
    for i in range(0, 2*t):
        for j in range(0, n):
            h[i].append((beta * (i + 1) * j) % (2**field_n - 1))

    for power in pT:
        # print("Encoding Type: ", n, k)
        print("Power: ", power)
        error = 0
        for sample in tqdm(range(1, samples)):
            msg = [random.randrange(2) for _ in range(k)]
            # print("Message vector:                  ", msg)
            codeword = encoder.encoder_31_11(msg)
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
            decoded = errorCorrection.berlekamp(field_n, n, t, GF, I_GF, h, codewordChannel)
            # print("Codeword after error correction: ",decoded)
            msgEst = decoded[n - k: ]
            # print("Decoded Message:                 ",msgEst)
            errPat = np.bitwise_xor(msg, msgEst)
            error += sum(errPat)
            # print()
        errRate.append(error / (k * sample))
    return errRate
# genErrRate(range(-16, -13), 2)
# plt.semilogy(range(-30, 20), rate)
# plt.show()