# def print_hello_world():
#     print("Hello, World!")

# print_hello_world()
# var = print_hello_world()
# print(var)

# def generate_squares(n):
#     return [i**2 for i in range(1, n+1)]

# squares = generate_squares(50)
# print(squares)

# def count_characters(str):
#     count = 0
#     for char in str:
#         count += 1
#     return count

# string = "Hello, World!"
# char_count = count_characters(string)
# print(f"The number of characters in the string is: {char_count}")

# def factorial(num):
#     if num == 1:
#         return 1
#     else:
#         return num * factorial(num - 1)

# num = 10
# print("Factorial of", num, "is:", factorial(num))

# def add(num1, num2):
#     return num1 + num2

# sum1 = add(100, 200)
# sum2 = add(8, 9)
# print(sum1)
# print(sum2)

# def generate_squares_0_to_50():
#     return [i**2 for i in range(51)]
# squares_0_to_50 = generate_squares_0_to_50()
# print(squares_0_to_50)

# def count_characters_loop(str):
#     count = 0
#     for char in str:
#         count += 1
#     return count
# string = "Hello, World! in python for class in B.tech CSE."
# char_count = count_characters_loop(string)
# print(f"The number of characters in the string is: {char_count}")

# def my_function(name):
#     print(name + " Ref")

# my_function("Emil")
# my_function("Tobias")
# my_function("Linus")

# def my_function_with_args(*kids):
#     print("The youngest child is " + kids[2])

# my_function_with_args("Emil", "Tobias", "Linus")

# def my_function(child3, child2, child1):
#     print("The youngest child is " + child3)

# my_function(child1="a", child2="b", child3="c")

# def my_function_with_kwargs(**kid):
#     print("His last name is " + kid["lname"])

# my_function_with_kwargs(name="T", lname="R")

# def my_function(country="Norway"):
#     print("I am from " + country)

# my_function("Sweden")
# my_function("India")
# my_function()
# my_function("Brazil")

# def my_function(food):
#     for x in food:
#         print(x)
#     print(type(food))

# fruits = ["apple", "banana", "cherry"]
# my_function(fruits)

# def my_function(x):
#     return 5 * x

# print(my_function(3))
# n = my_function(3)
# print(my_function(5))
# print(my_function(9))

# def myfunction():
#     pass

#Lamda function
# doubler = lambda x: x * 2
# print(doubler(2))

# var = lambda x, y: x * y
# print(var(2, 5))

# add_three_numbers = lambda x, y, z: x + y + z
# print(add_three_numbers(3, 4, 5))

# add = lambda *args: sum(args)
# print(add(2, 3, 5, 7))

# add = lambda **kwargs: sum(kwargs.values())
# print(add(x=2, y=3, z=3, f=8))

# findMin = lambda x, y: x if x < y else y
# print(findMin(2, 4))

# print(findMin('a', 'x'))

# is_even = lambda x: x % 2 == 0
# print(is_even(4)) 
# print(is_even(5))  

# reverse_string = lambda str: str[::-1]
# print(reverse_string("hello"))  

# max_num = lambda x, y: x if x > y else y
# print(max_num(10, 20))  # 20

# concat_strings = lambda s1, s2: s1 + s2
# print(concat_strings("Hello, ", "World!"))  

# square = lambda x: x ** 2
# print(square(5))  

# num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# even_numbers = list(filter(lambda x: x % 2 == 0, num))
# print(even_numbers)  

# squared_numbers = list(map(lambda x: x ** 2, num))
# print(squared_numbers) 

# tuples = [(1, 3), (2, 1), (3, 2)]
# sorted_tuples = sorted(tuples, key=lambda x: x[1])
# print(sorted_tuples)  

# length = lambda str: len(str)
# print(length("hello"))  

# to_uppercase = lambda str: str.upper()
# print(to_uppercase("hello")) 

# num = [1, 2, 3, 4, 5]
# doubled_num = list(map(lambda x: x * 2, num))
# print(doubled_num)  

# strings = ["hello", "world", "python"]
# uppercase_strings = list(map(lambda str: str.upper(), strings))
# print(uppercase_strings)  

# list1 = [1, 2, 3]
# list2 = [4, 5, 6]
# summed_lists = list(map(lambda x, y: x + y, list1, list2))
# print(summed_lists)
  

# num = [1, 2, 3, 4, 5]
# string_numbers = list(map(lambda x: str(x), num))
# print(string_numbers)  

# tuples = [(1, 2), (3, 4), (5, 6)]
# summed_tuples = list(map(lambda t: t[0] + t[1], tuples))
# print(summed_tuples)  

# defname = {7: 'sam', 8: 'john', 9: 'mathew', 10: 'riti', 11: 'aadi', 12: 'sachin'}
# defname = dict(map(lambda x: (x[0], x[1] + '_'), defname.items()))
# print('Modified Dictionary : ')
# print(defname)

# numbers = [5, 2, 9, 1, 5, 6]
# sorted_numbers = sorted(numbers)
# print(sorted_numbers)  

# strings = ["banana", "apple", "cherry"]
# sorted_strings = sorted(strings)
# print(sorted_strings)  

# tuples = [(1, 3), (2, 1), (3, 2)]
# sorted_tuples = sorted(tuples)
# print(sorted_tuples)

# sorted_tuples_by_second = sorted(tuples, key=lambda x: x[1])
# print(sorted_tuples_by_second)  

# dictionary = {3: 'three', 1: 'one', 2: 'two'}
# sorted_dict_keys = sorted(dictionary)
# print(sorted_dict_keys)  
# sorted_dict_values = sorted(dictionary.items(), key=lambda item: item[1])
# print(sorted_dict_values) 

# list_of_dicts = [{'name': 'John', 'age': 25}, {'name': 'Jane', 'age': 22}, {'name': 'Doe', 'age': 28}]
# sorted_list_of_dicts = sorted(list_of_dicts, key=lambda x: x['age'])
# print(sorted_list_of_dicts) 

