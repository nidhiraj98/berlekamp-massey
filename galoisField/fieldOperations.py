import math

def inverse(GF, I_GF, num):       #Compute inverse of a field element
    if num == 0:
        return 0
    n = int(math.log2(len(GF) + 1))
    key_of_num = I_GF[num]
    inv_key = ((2**n - 1) - key_of_num) % (2**n - 1)
    inv = GF[inv_key]
    return inv
    

def fieldMul(GF, I_GF, a, b):     #Multiply two elements in the field
    n = int(math.log2(len(GF) + 1))
    if a == 0 or b == 0:
        return 0
    alpha_a, alpha_b = I_GF[a], I_GF[b]
    p = GF[(alpha_a + alpha_b) % (2**n - 1)]
    return p


def computeSyndrome(GF, n, r, h, beta):      #Compute the syndrome of a given vector
    syndrome = 0
    for i in range(0, len(h)):
        if r[i] == 1:
            syndrome = syndrome ^ GF[h[i]]
    return syndrome
