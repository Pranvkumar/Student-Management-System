import numpy as np

# a. Convert numbers = [1, 2.0, 3] to a numpy array and convert all elements to string type.
numbers = [1, 2.0, 3]
numbers_array = np.array(numbers, dtype=str)
print(f"Array with string type elements: {numbers_array}\n")

# # b. Create a 2D array through a list and set dtype as int32.
# list_2d = [[1, 2, 3], [4, 5, 6]]
# array_2d = np.array(list_2d, dtype=np.int32)
# print(f"2D Array with dtype int32: {array_2d}\n")

# # c. Find the rows and columns of the 2D array created in part b.
# rows, cols = array_2d.shape
# print(f"Rows: {rows}, Columns: {cols}")

# # d. Print 10 random numbers between 1 and 100.
# random_numbers = np.random.randint(1, 101, size=10)
# print(f"10 Random Numbers between 1 and 100: {random_numbers}\n")

# # b) Write a NumPy program to test whether none of the elements of a given array is zero.
# array_test = np.array([1, 2, 3, 4])
# none_zero = np.all(array_test != 0)
# print(f"None of the elements is zero: {none_zero}")

# # c) Write a NumPy program to test whether any of the elements of a given array is non-zero.
# any_non_zero = np.any(array_test != 0)
# print(f"Any of the elements is non-zero: {any_non_zero}\n")

# # d) Write a NumPy program to generate an array of 15 random numbers from a standard normal distribution.
# random_normal_array = np.random.randn(15)
# print(f"Array of 15 random numbers from a standard normal distribution: {random_normal_array}")

# # a) Write a NumPy program to get help on the add function.
# print("Help on numpy.add function:")
# help(np.add)
