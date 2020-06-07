import numpy as np
from galoisField import fieldOperations as field

def receiver(n, length, t, GF, I_GF, h, rcvBlock):
    rcvBlock = np.transpose(rcvBlock).tolist()
    corrBlock = []
    for r in rcvBlock:
        # print(r)
        corrBlock.append(berlekamp(n, length, t, GF, I_GF, h, r))
    return corrBlock


def berlekamp(n, length, t, GF, I_GF, h, r):
    beta = int((2**n - 1)/length)
    syndromes = []
    for i in range(1, 2*t + 1):
        syndromes.append(field.computeSyndrome(GF, n, r, h[i - 1], beta))
    
    if syndromes == [0 for _ in range(2 * t)]:
        return r
    d_1 = syndromes[0]

    errLocTable = {
        'mu': [-0.5] + [i for i in range(0, t + 1)],
        'sigma': [[1], [1]],
        'd': [1, d_1],
        'l': [0, 0],
        'diff': [-1, 0]
    }

    for i in range(2, t + 2):
        mu = errLocTable['mu'][i - 1]

        if errLocTable['d'][i - 1] == 0: #Compute sigma
            sigma = errLocTable['sigma'][i - 1]
        else:
            p = errLocTable['mu'][errLocTable['diff'].index(max(errLocTable['diff'][:i - 1]))]
            d_u = errLocTable['d'][i - 1]
            d_p_inv = field.inverse(GF, I_GF, errLocTable['d'][errLocTable['mu'].index(p)])
            sigma_p = errLocTable['sigma'][errLocTable['mu'].index(p)]
            const = field.fieldMul(GF, I_GF, d_u, d_p_inv)
            big_term = [field.fieldMul(GF, I_GF, const, s) for s in sigma_p] + [0 for _ in range(int(2 * (mu - p)))]
            sigma_u = errLocTable['sigma'][i - 1]
            x = len(big_term) - len(sigma_u)
            sigma_u = [0 for _ in range(x)] + sigma_u
            sigma = list(np.bitwise_xor(big_term, sigma_u))

        l = len(sigma) - 1
        diff = 2 * errLocTable['mu'][i] - l

        errLocTable['sigma'].append(sigma)
        errLocTable['l'].append(l)
        errLocTable['diff'].append(diff)

        if(i == t + 1):
            break
        d = syndromes[2 * mu + 3 - 1] #initialize d
        for j in range(1, l + 1):   #compute d
            syn = syndromes[2 * mu + 3 - 1 - j]
            curr = field.fieldMul(GF,I_GF,  syn, sigma[l - j])
            d ^= curr
        errLocTable['d'].append(d)

    errLocPoly = errLocTable['sigma'][t + 1]

    # print(errLocPoly)
    if len(errLocPoly) - 1 <= t:
        errLocPoly.reverse()
        errLoc = []
        for i in range(0, 2**n - 1):
            sum = 0
            for j in range(0, len(errLocPoly)):
                sum ^= field.fieldMul(GF, I_GF, errLocPoly[j], GF[(i * j) % (2**n - 1)])
            if sum == 0:
                if i == 0:
                    errLoc.append(1)
                else:
                    errLoc.append((2**n - 1) - i)
        # print(errLoc)
        for i in errLoc:
            if int(i/beta) >= length:
                continue
            r[int(i/beta)] ^= 1
        return r