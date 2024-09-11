# Based on https://github.com/AllAlgorithms, python/algorithms/math/anagram_check.py

# function to check if two strings are
# anagram or not  
def anagram_check(s1: str, s2: str) -> bool:
    if len(s1) == 1 and len(s2) == 1:
        return s1 == s2
    if len(s1) != len(s2):
        return False

    # the sorted strings are checked
    if ''.join(sorted(s1)) == ''.join(sorted(s2)):
        return True
    else:
        return False
