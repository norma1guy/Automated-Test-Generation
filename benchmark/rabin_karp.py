# Based on https://github.com/AllAlgorithms, python/algorithms/math/rabin_karp.py


# Rabin Karp Algorithm in python using hash values


def rabin_karp_search(pat: str, txt: str) -> list:
    assert len(pat) <= len(txt)

    # d is the number of characters in input alphabet
    d = 2560
    q = 101

    M = len(pat)
    N = len(txt)
    i = 0
    j = 0

    p = 0
    t = 0
    h = 1

    for i in range(M - 1):
        h = (h * d) % q

    for i in range(M):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q

    found_at_index = []
    for i in range(N - M + 1):
        if p == t:
            for j in range(M):
                if txt[i + j] != pat[j]:
                    break

            j += 1
            if j == M:
                found_at_index.append(i)

        if i < N - M:
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q
            if t < 0:
                t = t + q

    return found_at_index
