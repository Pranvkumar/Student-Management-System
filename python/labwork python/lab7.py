# num =list (map(int, input("Enter number to add : ").split()))
# sum = sum(num)
# print(f"This sum of all elements {sum}")


# age = list(map(int, input("Enter ages: ").split()))
# adults = filter(lambda x: x > 18, age)
# print(f"This list of adult{list(adults)}")

# dict1 = {input("Enter name: ").strip(): int(input("Enter age: ")) for _ in range(int(input("Enter number of students: ")))}
# dict_age = dict(sorted(dict1.items(), key=lambda item: item[1]))
# dict_name = dict(sorted(dict1.items(), key=lambda item: item[0]))
# print(dict_name)
# print(dict_age)

# def make_multiplier_of(n):
#     def multiplier(x):
#         return x * n
#     return multiplier
# times_three = make_multiplier_of(3)
# print(f"3 times 5 is {times_three(5)}")
