# Day 13 Question 2
from collections import Counter

def can_form_palindrome(s):
    freq = Counter(s)
    odd_count = sum(1 for v in freq.values() if v % 2 != 0)
    return odd_count <= 1
# Example usage:
if __name__ == "__main__":
    # Q2 Examples
    examples_q2 = [
        "aab",
        "abc",
        "aabbcc"
    ]
    for ex in examples_q2:
        result = can_form_palindrome(ex)
        print(f'Input: "{ex}"')
        print(f'Output: {str(result).lower()}\n')
