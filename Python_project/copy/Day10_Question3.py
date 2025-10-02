# 3. Check Anagram
def are_anagrams(str1, str2):
    s1 = ''.join(str1.lower().split())
    s2 = ''.join(str2.lower().split())
    return sorted(s1) == sorted(s2)

anagram_examples = [
    ("listen", "silent"),
    ("hello", "world"),
    ("The Eyes", "They See")
    ]
for s1, s2 in anagram_examples:
    result = are_anagrams(s1, s2)
    print(f'Input: String1: "{s1}", String2: "{s2}"')
    print(f'Output:\n{str(result).lower()}\n')