import time
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(20000)

def binary_search_recursive(arr, left, right, key):
    if left > right:
        return -1
    mid = left + (right - left) // 2
    if arr[mid] == key:
        return mid
    elif arr[mid] > key:
        return binary_search_recursive(arr, left, mid - 1, key)
    else:
        return binary_search_recursive(arr, mid + 1, right, key)


def binary_search_iterative(arr, key):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] > key:
            right = mid - 1
        else:
            left = mid + 1
    return -1



sizes = [10*3, 104, 105, 106, 5*106, 10*7]  
recursive_times = []
iterative_times = []

for n in sizes:
    arr = list(range(n))  
    key = n - 1            


    start = time.time()
    binary_search_recursive(arr, 0, n - 1, key)
    end = time.time()
    recursive_times.append(end - start)

   
    start = time.time()
    binary_search_iterative(arr, key)
    end = time.time()
    iterative_times.append(end - start)


plt.figure(figsize=(10, 6))
plt.plot(sizes, recursive_times, marker='o', label="Recursive Binary Search")
plt.plot(sizes, iterative_times, marker='s', label="Iterative Binary Search")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.title("Binary Search: Recursive vs Iterative (Time Complexity Analysis)")
plt.legend()
plt.grid(True)
plt.show()


# import time
# import matplotlib.pyplot as plt
# import sys

# sys.setrecursionlimit(20000)

# def binary_search_recursive(arr, left, right, key):
#     if left > right:
#         return -1
#     mid = left + (right - left) // 2
#     if arr[mid] == key:
#         return mid
#     elif arr[mid] > key:
#         return binary_search_recursive(arr, left, mid - 1, key)
#     else:
#         return binary_search_recursive(arr, mid + 1, right, key)

# def binary_search_iterative(arr, key):
#     left, right = 0, len(arr) - 1
#     while left <= right:
#         mid = left + (right - left) // 2
#         if arr[mid] == key:
#             return mid
#         elif arr[mid] > key:
#             right = mid - 1
#         else:
#             left = mid + 1
#     return -1

# # Use smaller sizes to avoid memory errors and recursion depth issues
# sizes = [10**4, 10**5, 10**6, 10**7]
# recursive_times = []
# iterative_times = []

# for n in sizes:
#     arr = list(range(n))
#     key = n - 1

#     # Recursive
#     start = time.perf_counter()
#     binary_search_recursive(arr, 0, n - 1, key)
#     end = time.perf_counter()
#     recursive_times.append(end - start)

#     # Iterative
#     start = time.perf_counter()
#     binary_search_iterative(arr, key)
#     end = time.perf_counter()
#     iterative_times.append(end - start)

# plt.figure(figsize=(10, 6))
# plt.plot(sizes, recursive_times, marker='o', label="Recursive Binary Search")
# plt.plot(sizes, iterative_times, marker='s', label="Iterative Binary Search")
# plt.xlabel("Input Size (n)")
# plt.ylabel("Time (seconds)")
# plt.title("Binary Search: Recursive vs Iterative (Time Complexity Analysis)")
# plt.legend()
# plt.grid(True)
# plt.xscale('log')
# plt.show()