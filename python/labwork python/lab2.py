import math


# num1 = float(input("Enter first number: "))
# num2 = float(input("Enter second number: "))
# num3 = float(input("Enter second number: "))
# sum = num1 + num2 + num3
# print("The sum of {0} and {1} is {2}".format(num1, num2, sum))

# str1 = input("Enter first string: ")
# str2 = input("Enter second string: ")
# result = str1 + " " + str2
# print(result)

# length = float(input("Enter the length of the rectangle: "))
# width = float(input("Enter the width of the rectangle: "))
# area = length * width
# print("The area of the rectangle is:", area)

# radius = float(input("Enter the radius of the circle: "))
# area = math.pi * radius ** 2
# print("The area of the circle is:", area)

# number = float(input("Enter a number: "))
# cubic_root = number ** (1/3)
# print("The cubic root of {0} is {1}".format(number, cubic_root))

# num1 = float(input("Enter first number: "))
# num2 = float(input("Enter second number: "))
# num3 = float(input("Enter third number: "))
# average = (num1 + num2 + num3) / 3
# print("The average of {0}, {1}, and {2} is {3}".format(num1, num2, num3, average))

# num1 = float(input("Enter first number: "))
# num2 = float(input("Enter second number: "))
# num1 = num1 - num2
# num2 = num1 + num2
# num1 = num2 - num1
# print("After swapping, first number is:", num1)
# print("After swapping, second number is:", num2)

# user_string = input("Enter a string: ")
# uppercase_string = user_string.upper()
# print("Uppercase:", uppercase_string)
# lowercase_string = user_string.lower()
# print("Lowercase:", lowercase_string)
# length_of_string = len(user_string)
# print("Length of the string:", length_of_string)
# reversed_string = user_string[::-1]
# print("Reversed string:", reversed_string)
# is_palindrome = user_string == reversed_string
# print("Is the string a palindrome?", is_palindrome)

# number = int(input("Enter a number: "))
# if number % 2 == 0:
#     print("{0} is Even".format(number))
# else:
#     print("{0} is Odd".format(number))

# marks = []
# for i in range(5):
#     mark = float(input(f"Enter marks for subject {i+1}: "))
#     marks.append(mark)

# average_marks = sum(marks) / len(marks)
# print("Average marks:", average_marks)

# if 91 <= average_marks <= 100:
#     grade = 'O'
# elif 81 <= average_marks <= 90:
#     grade = 'A+'
# elif 71 <= average_marks <= 80:
#     grade = 'A'
# elif 61 <= average_marks <= 70:
#     grade = 'B+'
# elif 51 <= average_marks <= 60:
#     grade = 'B'
# elif 41 <= average_marks <= 50:
#     grade = 'C+'
# elif 35 <= average_marks <= 40:
#     grade = 'C'
# else:
#     grade = 'Fails'

# print("Grade:", grade)

#2a

# n = int(input("Enter a number: "))
# if n % 2 != 0:
#     print("Weird")
# elif 2 <= n <= 5:
#     print("Not Weird")
# elif 6 <= n <= 20:
#     print("Weird")
# else:
#     print("Not Weird")

# n = int(input("Enter a number: "))
# for i in range(n):
#     print(i ** 2)

# n = int(input("Enter a number: "))
# for i in range(1, n + 1):
#     print(i, end="")

# i = 1
# while i <= 9:
#     print((str(i) + ' ') * i)
#     i += 2

# n = 5
# for i in range(n, 0, -1):
#     for j in range(i):
#         print(i, end=" ")
#     print()

# n = 5
# for i in range(n, 0, -1):
#     for j in range(i, 0, -1):
#         print(j, end=" ")
#     print()

# n = 5
# for i in range(n, 0, -1):
#     for j in range(i):
#         print("*", end=" ")
#     print()