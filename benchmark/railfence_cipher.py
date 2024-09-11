# Based on https://github.com/AllAlgorithms, python/algorithms/math/railfence_cipher.py


def railencrypt(st: str, k: int) -> str:
    assert k > 1
    c = 0
    x = 0
    m =[[0] * (len(st)) for i in range(k)]
    for r in range(len(st)):
        m[c][r] = ord(st[r])
        if x == 0:
            if c == (k-1):
                x = 1
                c -= 1
            else:
                c += 1
        else:
            if c == 0:
                x = 0
                c += 1
            else:    
                c -= 1
           
    result = [] 
    for i in range(k): 
        for j in range(len(st)): 
            if m[i][j] != 0: 
                    result.append(chr(m[i][j]))
    return ''.join(result)


def raildecrypt(st: str, k: int) -> str:
    assert k > 1
    c , x = 0 , 0
    m =[[0] * (len(st)) for i in range(k)]
    for r in range(len(st)):
        m[c][r] = 1
        if x == 0:
            if c == (k-1):
                x = 1
                c -= 1
            else:
                c += 1
        else:
            if c == 0:
                x = 0
                c += 1
            else:    
                c -= 1
    result = []
    c , x = 0 , 0
    for i in range(k): 
        for j in range(len(st)): 
            if m[i][j] == 1:
                m[i][j] = ord(st[x])
                x += 1
    for r in range(len(st)):
        if m[c][r] != 0:
            result.append(chr(m[c][r]))
        if x == 0:
            if c == (k-1):
                x = 1
                c -= 1
            else:
                c += 1
        else:
            if c == 0:
                x = 0
                c += 1
            else:    
                c -= 1
    return ''.join(result)

