def count_vowels_consonants(string):
    vowels = set('aeiou')
    vowels_count = 0
    consonants_count = 0
    for consonants in string.lower():
        if consonants.isalpha():
            if consonants in vowels:
                vowels_count += 1
            else:
                consonants_count += 1
    return vowels_count, consonants_count

# 2. Count vowels and consonants
string = input("Enter a string to count vowels and consonants: ")
vowels, consonants = count_vowels_consonants(string)
print(f'"{string}" -> Vowels: {vowels}, Consonants: {consonants}')