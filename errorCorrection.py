import numpy as np
# import generateField
import fieldOperations as field

# n = 5
# t = 5   #Error Correcting Capability

# r = [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   #received vector

def receiver(n, t, GF, rcvBlock):
    rcvBlock = np.transpose(rcvBlock).tolist()
    corrBlock = []
    # print("Here")
    # GF = generateField.field(n)
    # print("GF Generated")
    for r in rcvBlock:
        # print(r)
        corrBlock.append(berlekamp(n, t, GF, r))
    return corrBlock


def berlekamp(n, t, GF, r):
    syndromes = []
    for i in range(2*t):
        syndromes.append(field.computeSyndrome(GF, r, i + 1))
    # print(syndromes)
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
            d_p_inv = field.inverse(GF, errLocTable['d'][errLocTable['mu'].index(p)])
            sigma_p = errLocTable['sigma'][errLocTable['mu'].index(p)]
            const = field.fieldMul(GF, d_u, d_p_inv)
            big_term = [field.fieldMul(GF, const, s) for s in sigma_p] + [0 for _ in range(int(2 * (mu - p)))]
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
            curr = field.fieldMul(GF, syn, sigma[l - j])
            d ^= curr
        errLocTable['d'].append(d)


    errLocPoly = errLocTable['sigma'][t + 1]
    if len(errLocPoly) - 1 <= t:
        errLocPoly.reverse()
        errLoc = []
        for i in range(0, 2**n - 1):
            sum = 0
            for j in range(0, len(errLocPoly)):
                sum ^= field.fieldMul(GF, errLocPoly[j], GF[(i * j) % (2**n - 1)])
            if sum == 0:
                errLoc.append((2**n - 1) - i)

        for i in errLoc:
            r[i] ^= 1
        return r
    else:
        return "Message Corrupted. Request Retransmission"