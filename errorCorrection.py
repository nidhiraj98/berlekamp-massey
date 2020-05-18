import numpy as np
import generateField
import fieldOperations as field

n = 5
t = 5   #Error Correcting Capability

r = [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   #received vector

def main():
    GF = generateField.field(n)
    syndromes = []
    for i in range(2*t):
        syndromes.append(field.computeSyndrome(GF, r, i + 1))
    print(syndromes)
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
            # print("p = ", p)
            d_u = errLocTable['d'][i - 1]
            # print("du = ", d_u)
            d_p_inv = field.inverse(GF, errLocTable['d'][errLocTable['mu'].index(p)])
            # print("dp = ", d_p_inv)
            sigma_p = errLocTable['sigma'][errLocTable['mu'].index(p)]
            # print("sigma_p = ", sigma_p)
            const = field.fieldMul(GF, d_u, d_p_inv)
            big_term = [field.fieldMul(GF, const, s) for s in sigma_p] + [0 for _ in range(int(2 * (mu - p)))]
            # print("bigterm = ", big_term)
            sigma_u = errLocTable['sigma'][i - 1]
            x = len(big_term) - len(sigma_u)
            sigma_u = [0 for _ in range(x)] + sigma_u
            sigma = list(np.bitwise_xor(big_term, sigma_u))
            # print("sigma = ", sigma)

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
            # print("curr, d = ", curr, d)
            d ^= curr
            # print("d = ", d)
        errLocTable['d'].append(d)

    # print(errLocTable)

    errLocPoly = errLocTable['sigma'][t + 1]
    # print(errLocPoly)
    if len(errLocPoly) - 1 <= t:
        errLocPoly.reverse()
        errLoc = []
        for i in range(0, 2**n - 1):
            sum = 0
            for j in range(0, len(errLocPoly)):
                sum ^= field.fieldMul(GF, errLocPoly[j], GF[(i * j) % (2**n - 1)])
            if sum == 0:
                errLoc.append((2**n - 1) - i)

        # print(errLoc)
        for i in errLoc:
            r[i] ^= 1
        print("Message Sent: ", r)
    else:
        print("Message Corrupted. Request Retransmission")

if __name__ == "__main__":
    main()