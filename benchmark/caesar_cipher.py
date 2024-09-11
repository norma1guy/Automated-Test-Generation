# Based on https://github.com/AllAlgorithms, python/algorithms/math/caesar_cipher.py


def encrypt(strng: str, key: int) -> str:
    assert 0 < key <= 94
    encrypted = ''
    for x in strng:
        indx = (ord(x) + key) % 256
        if indx > 126:
            indx = indx - 95
        encrypted = encrypted + chr(indx)
    return encrypted


def decrypt(strng: str, key: int) -> str:
    assert 0 < key <= 94
    decrypted = ''
    for x in strng:
        indx = (ord(x) - key) % 256
        if indx < 32:
            indx = indx + 95
        decrypted = decrypted + chr(indx)
    return decrypted


