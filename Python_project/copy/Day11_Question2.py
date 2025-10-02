# 2. Longest Palindromic Substring
def longest_palindromic_substring(input_string: str) -> str:
    string_length = len(input_string)
    if string_length == 0:
        return ""
    start_index, maximum_length = 0, 1
    dynamic_programming = [[False]*string_length for _ in range(string_length)]
    for index in range(string_length):
        dynamic_programming[index][index] = True
    for index in range(string_length-1):
        if input_string[index] == input_string[index+1]:
            dynamic_programming[index][index+1] = True
            start_index = index
            maximum_length = 2
    for current_length in range(3, string_length+1):
        for left_index in range(string_length-current_length+1):
            right_index = left_index+current_length-1
            if input_string[left_index] == input_string[right_index] and dynamic_programming[left_index+1][right_index-1]:
                dynamic_programming[left_index][right_index] = True
                start_index = left_index
                maximum_length = current_length
    return input_string[start_index:start_index+maximum_length]

if __name__ == "__main__":
    print(longest_palindromic_substring("babad"))  
    print(longest_palindromic_substring("cbbd"))  
    print(longest_palindromic_substring("racecar")) 
