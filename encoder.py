import numpy as np

def encoder_31_11(info):
    n = 31
    k = 11
    genLoc = [20, 18, 17, 13, 10, 9, 7, 6, 4, 2, 0]
    gen = [0 for _ in range(n - k + 1)]
    for i in genLoc:
        gen[i] = 1
    msg = []
    for i in range(0, len(info)):
        msg.append(int(info[i]))
    # print(msg)
    x = msg + [0 for _ in range(0, n - k)]
    # x = np.polymul(msg, x_nk)
    [q, rem] = np.polydiv(x, gen)
    for i in range(0, len(rem)):
        rem[i] = abs(rem[i] % 2)
    if(len(rem) < n - k):
        rem = np.flip(rem).tolist()
        while(len(rem) < n - k):
            rem.append(0)
        rem = np.flip(rem)	
    	
    return rem.astype(int).tolist() + msg

def encoder_51_19(info):
    n = 51
    k = 19
    genLoc = [0, 1, 3, 5, 6, 8, 9, 10, 11, 12, 14, 16, 19, 21, 24, 30, 32]
    gen = [0 for _ in range(n - k + 1)]
    for i in genLoc:
        gen[i] = 1
    msg = []
    for i in range(0, len(info)):
        msg.append(int(info[i]))
    x_nk = [1] + [0 for _ in range(0, n - k)]
    x = np.polymul(msg, x_nk)
    [q, rem] = np.polydiv(x, gen)
    for i in range(0, len(rem)):
        rem[i] = abs(rem[i] % 2)
    if(len(rem) < n - k):
        rem = np.flip(rem).tolist()
        while(len(rem) < n - k):
            rem.append(0)
        rem = np.flip(rem)		
    code_word = rem.astype(int).tolist() + msg
    return code_word

def encoder_51_27(info):
    n = 51
    k = 27
    genLoc = [0, 1, 5, 8, 9, 12, 13, 15, 17, 20, 21, 22, 24]
    gen = [0 for _ in range(n - k + 1)]
    for i in genLoc:
        gen[i] = 1
    msg = []
    for i in range(0, len(info)):
        msg.append(int(info[i]))
    x_nk = [1] + [0 for _ in range(0, n - k)]
    x = np.polymul(msg, x_nk)
    [q, rem] = np.polydiv(x, gen)
    for i in range(0, len(rem)):
        rem[i] = abs(rem[i] % 2)
    if(len(rem) < n - k):
        rem = np.flip(rem).tolist()
        while(len(rem) < n - k):
            rem.append(0)
        rem = np.flip(rem)		
    code_word = rem.astype(int).tolist() + msg
    return code_word