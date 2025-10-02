from collections import OrderedDict

def first_non_repeating_char(string):
    freq = OrderedDict()
    for consonants in string:
        freq[consonants] = freq.get(consonants, 0) + 1
    for consonants in freq:
        if freq[consonants] == 1:
            return consonants
    return -1

# 3. First non-repeating character
string = input("Enter a string to find the first non-repeating character: ")
result = first_non_repeating_char(string)
print(f'First non-repeating character in "{string}": {result}')