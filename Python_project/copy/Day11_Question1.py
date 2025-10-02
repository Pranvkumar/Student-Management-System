import re

# 1. Palindrome Ignoring Spaces and Punctuation
def is_palindrome(input_string: str) -> bool:
    filtered_string = re.sub(r'[^a-z,A-Z,0-9]', '', input_string).lower()
    return filtered_string == filtered_string[::-1]

if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama")) 
    print(is_palindrome("race a car"))  
    print(is_palindrome("Was it a car or a cat I saw?"))  
