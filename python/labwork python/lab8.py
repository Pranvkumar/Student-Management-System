import random
import math
import file1

# (1) Python program to use try-except-else block
def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    else:
        print(f"Result: {result}")

divide_numbers(10, 2)
divide_numbers(10, 0)

# (2) Python program to use try-except-finally block
def read_file(file_name):
    try:
        file1 = open(file_name, 'r')
        content = file1.read()
        print(content)
    except FileNotFoundError:
        print("Error: File not found.")
    finally:
        print("Execution completed.")

read_file("example.txt")

# (3) Python program to write your own exception and throw it
class CustomException(Exception):
    pass

def check_positive(number):
    if number < 0:
        raise CustomException("Negative number is not allowed.")
    else:
        print(f"{number} is positive.")

try:
    check_positive(-5)
except CustomException as e:
    print(e)

# (4) Python program to demonstrate the use of built-in modules random and math

lower_bound = int(input("Enter the lower bound for random number: "))
upper_bound = int(input("Enter the upper bound for random number: "))
random_number = random.randint(lower_bound, upper_bound)
print(f"Random number between {lower_bound} and {upper_bound}: {random_number}")


number = float(input("Enter a number to find its square root: "))
square_root = math.sqrt(number)
print(f"Square root of {number}: {square_root}")

# (5) Program to create a module and use its functionality
print(file1.greet("Pranvkumar"))