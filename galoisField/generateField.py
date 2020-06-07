def field(n = 4):
    GF = {}
    I_GF = {}
    GF[0] = 0b1
    for i in range(1, n):
        # print(i)
        GF[i] = GF[i - 1] << 1
    for i in range(n, 2**n - 1):
        # print(i)
        if n == 8: 
            GF[i] = GF[i - n] ^ GF[i - n + 2] ^ GF[i - n + 3] ^ GF[i - n + 4]   #GF(2^8)
        elif n == 7:
            GF[i] = GF[i - n] ^ GF[i - n + 3] #GF(2^7)
        elif n == 6:
            GF[i] = GF[i - n] ^ GF[i - n + 1] #GF(2^6)
        elif n == 5:
            GF[i] = GF[i - n] ^ GF[i - n + 2] #GF(2^5)
        elif n == 4:
            GF[i] = GF[i - n] ^ GF[i - n + 1] #GF(2^4)
        elif n == 3:
            GF[i] = GF[i - n] ^ GF[i - n + 1] #GF(2^3)

    # for i, gf_val in enumerate(GF):
    #     I_GF[gf_val] = i
    I_GF = {v:k for k,v in GF.items()}
    return GF, I_GF