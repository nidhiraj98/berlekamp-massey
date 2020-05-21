import math

def inverse(GF, num):       #Compute inverse of a field element
    if num == 0:
        return 0
    n = int(math.log2(len(GF) + 1))
    for key, val in GF.items():
        if val == num:
            inv_key = ((2**n - 1) - key) % (2**n - 1)
            break
    inv = GF[inv_key]
    return inv
    

def fieldMul(GF, a, b):     #Multiply two elements in the field
    n = int(math.log2(len(GF) + 1))
    if a == 0 or b == 0:
        return 0
    for key, val in GF.items():
        if val == a:
            alpha_a = key
        if val == b:
            alpha_b = key
    p = GF[(alpha_a + alpha_b) % (2**n - 1)]
    return p

def computeSyndrome(GF, n, r, x, beta):      #Compute the syndrome of a given vector
    h = []
    for i in range(0, len(r)):
        h.append((beta * x * i) % (2**n - 1))
    syndrome = 0
    for i in range(0, len(h)):
        if r[i] == 1:
            syndrome = syndrome ^ GF[h[i]]
    return syndrome
