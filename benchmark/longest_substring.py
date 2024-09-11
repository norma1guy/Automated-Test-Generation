# Based on https://github.com/AllAlgorithms, python/algorithms/math/longest_substring.py

# Create an algorithm that prints the longest substring of s in which
# the letters occur in alphabetical order. For example, if
# s = 'azcbobobegghakl', then your program should print:
# Longest substring in alphabetical order is: beggh

# In the case of ties, print the first substring.
# For example, if s = 'abcbcd', then your program should print:
# Longest substring in alphabetical order is: abc


def longest_sorted_substr(s: str) -> str:
    count = 0
    max_count = 0
    end_position = 0
    for char in range(len(s) - 1):
        if (s[char] <= s[char + 1]):
            count += 1
            if count > max_count:
                max_count = count
                end_position = char + 1
        else:
            count = 0
    start_position = end_position - max_count
    return s[start_position:end_position+1]


