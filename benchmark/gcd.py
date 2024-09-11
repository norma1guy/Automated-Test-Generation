# Based on https://github.com/AllAlgorithms, python/algorithms/math/common_divisor_count.py

def gcd(a: int, b: int) -> int:
    assert a > 0 and b > 0
    if a == 1 or b == 1:
        return 1
    if a == b:
        return a
    if b > a:
        a, b = b, a
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a
