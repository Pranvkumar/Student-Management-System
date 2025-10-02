# 3. Count Palindromic Substrings
def count_palindromic_substrings(input_string: str) -> int:
    string_length = len(input_string)
    palindrome_count = 0
    for center_index in range(2*string_length-1):
        left_pointer = center_index // 2
        right_pointer = left_pointer + center_index % 2
        while left_pointer >= 0 and right_pointer < string_length and input_string[left_pointer] == input_string[right_pointer]:
            palindrome_count += 1
            left_pointer -= 1
            right_pointer += 1
    return palindrome_count

if __name__ == "__main__":
    print(count_palindromic_substrings("abc"))
    print(count_palindromic_substrings("aaa")) 
    print(count_palindromic_substrings("aba"))  