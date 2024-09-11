# Based on https://github.com/AllAlgorithms, python/algorithms/math/exponentiation.py

def exponentiation(baseNumber: int, power: int) -> float:
    assert not (baseNumber == 0 or power <= 0)

    answer = None
    
    if power > 1:
        halfAnswer = exponentiation(baseNumber, power//2)
        answer = halfAnswer * halfAnswer
        
        if power%2 == 1:
            answer *= baseNumber
    
    elif power == 1:
        answer = baseNumber
    
    elif power == 0:
        answer = 1
    
    else: # negative power
        answer = 1 / exponentiation(baseNumber, abs(power))
    
    return answer
