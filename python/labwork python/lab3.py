# def check_number():
#     num = int(input("Enter a number: "))
    
#     # Check even or odd
#     if num % 2 == 0:
#         print(f"{num} is even.")
#     else:
#         print(f"{num} is odd.") 
#     # Check prime or non-prime
#     if num > 1:
#         for i in range(2, num):
#             if (num % i) == 0:
#                 print(f"{num} is not a prime number.")
#                 break
#         else:
#             print(f"{num} is a prime number.")
#     else:
#         print(f"{num} is not a prime number.")


# def print_string():
#     user_string = input("Enter a string: ")
    
#     print("Forward order:")
#     for char in user_string:
#         print(char, end=' ')
#     print()
    
#     print("Reverse order:")
#     for i in range(len(user_string)-1, -1, -1):
#         print(user_string[i], end=' ')
#     print()


# def count_substring():
#     main_string = input("Enter the main string: ")
#     sub_string = input("Enter the substring: ")
    
#     count = 0
#     sub_len = len(sub_string)
    
#     for i in range(len(main_string) - sub_len + 1):
#         if main_string[i:i+sub_len] == sub_string:
#             count += 1
    
#     print(f"The substring '{sub_string}' occurs {count} times in the main string.")

# # Function calls
# check_number()
# print_string()
# count_substring()


# def print_initials():
#     full_name = input("Enter the full name: ")
#     name_parts = full_name.split()
    
#     if len(name_parts) >= 3:
#         first_name, middle_name, last_name = name_parts[0], name_parts[1], name_parts[2]
#         initials = f"{first_name[0].upper()}.{middle_name[0].upper()}."
#         print(f"{initials} {last_name.capitalize()}")
#     else:
#         print("Please enter a first name, middle name, and last name.")


# def count_alphabets():
#     input_string = input("Enter a string: ").lower()
#     alphabet_count = {}
    
#     for char in input_string:
#         if char.isalpha():
#             if char in alphabet_count:
#                 alphabet_count[char] += 1
#             else:
#                 alphabet_count[char] = 1
    
#     for char in sorted(alphabet_count):
#         print(f"{alphabet_count[char]}{char.upper()}")

# # Function calls
# # print_initials()
# count_alphabets()