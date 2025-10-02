def is_palindrome(string):
    checker = ''.join([consonants.lower() for consonants in string if consonants.isalpha()])
    return checker == checker[::-1]

# 1. Palindrome check
string = input("Enter a string to check if it's a palindrome: ")
print(f'Is "{string}" a palindrome :  {is_palindrome(string)}')   