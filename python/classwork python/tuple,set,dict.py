# score = (20,21,23,45)
# print(score)
# # score[2] = 22 here is error

# score = score * 2
# score1 = (12,23,34,45)
# score1 = score1 + score
# print(score)
# print(score1)
# print(len(score))
# score = score.count(12)
# print(score)
# score1 = score1.index(12)
# print(score1)

#set 
# set1 = {1,2,3,4,5,5,6}
# print(set1)
# set2 = set([1,2,3,4,5,5])
# print(set2)
# print(type(set1))
# print(2 in set2)
# set1.add(23)
# print(set1)
# set1.remove()


# dictionary
# t = {
#     "brand": "Ford",
#     "model": "Mustang",
#     "year": 1964
# }
# m = t.copy()
# print(m)

# t["year"] = 2020
# print(t)
# print(m)

# t["color"] = "red"
# print(t)

# del t["model"]
# print(t)

# for key, value in t.items():
#     print(f"{key}: {value}")

# thisdict = {
#     "brand": "Ford",
#     "model": "Mustang",
#     "year": 1964
# }
# del thisdict

# thisdict = {
#     "brand": "Ford",
#     "model": "Mustang",
#     "year": 1964
# }
# thisdict.clear()
# print(thisdict)  
# thisdict = {
#     "brand": "Ford",
#     "model": "Mustang",
#     "year": 1964
# }
# thisdict.popitem()
# print(thisdict)


# my_info = {'name': 'Rahul', 'age': 25}
# my_info['age'] = 26
# print(my_info)

# thisdict = {
#     "brand": "Ford",
#     "model": "Mustang",
#     "year": 1964
# }
# thisdict["color"] = "red"
# print(thisdict)  

#comprehensions
input_list = [1, 2, 3, 4, 4, 5, 6, 7, 7]
output_list = [var for var in input_list if var % 2 == 0]
print("Output List using for loop:", output_list)

input_list = [10, 20, 30, 40, 50, 60, 70]
list_using_comp = [var for var in input_list if var % 3 == 0]
print("Output List using list comprehensions:", list_using_comp)

input_numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 11]
even_numbers_set_comp = {num for num in input_numbers if num % 2 == 0}
print("Output Set using set comprehensions:", even_numbers_set_comp)