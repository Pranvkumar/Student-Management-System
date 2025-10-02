# Example 1: Handling a specific exception
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You can't divide by zero!")

# Example 2: Handling multiple exceptions
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You can't divide by zero!")
except TypeError:
    print("Invalid type!")

# Example 3: Using else and finally
try:
    result = 10 / 2
except ZeroDivisionError:
    print("You can't divide by zero!")
else:
    print("The result is:", result)
finally:
    print("This block is always executed.")

# Example 4: Raising an exception
try:
    raise ValueError("This is a custom error message")
except ValueError as e:
    print("Caught an exception:", e)

# Example 5: Custom exception
class CustomError(Exception):
    pass

try:
    raise CustomError("This is a custom error")
except CustomError as e:
    print("Caught a custom exception:", e)