# add = lambda x, y: x + y
# print(add(2, 3))  

# numbers = [1, 2, 3, 4, 5]
# squared = list(map(lambda x: x ** 2, numbers))
# print(squared)  

# even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
# print(even_numbers)

# points = [(2, 3), (1, 2), (4, 1), (3, 5)]
# points_sorted = sorted(points, key=lambda point: point[1])
# print(points_sorted)  

# max_value = lambda a, b: a if a > b else b
# print(max_value(10, 20))

# words = ["programming","pranav","tanmay"]
# uppercased_words = list(map(lambda word: word.upper(), words))
# print(uppercased_words)

# students = {'ranjan': 85, 'Bob': 92, 'tanmay': 78}
# passed_students = {name: grade for name, grade in students.items() if grade >= 80}
# print(passed_students)

# words = ["programming", "pranav", "tanmay"]
# sorted_words = sorted(words, key=lambda word: len(word))
# print(sorted_words)

# words = ["e", "a", "i", "o", "u"]
# sorted_alphabetically = sorted(words)
# print(sorted_alphabetically)

# py_set = {'e', 'a', 'u', 'o', 'i'}
# print(sorted(py_set, reverse=True))

# py_dict = {'e': 1, 'a': 2, 'u': 3, 'o': 4, 'i': 5}
# print(sorted(py_dict, reverse=True))

# item = ["S", "SS", "aaaa", "cc"]
# sorted_item = sorted(item, key=len)
# print(sorted_item)

# def func(x):
#     return x % 7
# L = [15, 3, 11, 7]
# print("Normal sort:", sorted(L))
# print("Sorted with key:", sorted(L, key=func))

# dict = {}
# dict['1'] = 'apple'
# dict['3'] = 'orange'
# dict['2'] = 'mango'
# lst = dict.values()
# print("Sorted by value: ", sorted(lst))
# print("Sorted by key: ", sorted(dict.items()))

# def checkAge(age):
#     return age > 18

# age = [5, 11, 16, 19, 24, 42]
# adults = filter(checkAge, age)
# print(list(adults))

# age = [5, 11, 16, 19, 24, 42]
# adults = filter(lambda x: x > 18, age)
# print(list(adults))

# def outer_function(x):
#     def inner_function(y):
#         return x + y
#     return inner_function

# add_five = outer_function(5)
# print(add_five(10))  

# def make_multiplier_of(n):
#     def multiplier(x):
#         return x * n
#     return multiplier

# times_three = make_multiplier_of(3)
# print(times_three(9)) 

# def outer(name):
#     def inner():
#         print(name)
#     inner()
# outer("pranav")

# x = "global"

# def my_function():
#     x = "local"
#     print("Inside function:", x)

# my_function()
# print("Outside function:", x)

letters = ['a', 'e', 'd', 'f', 'g', 't', 'I', 'c', 'w']
list1 = ['a','i','0','u','e']
vowels = filter(lambda x: x.lower() in list1, letters)
print(list(vowels))