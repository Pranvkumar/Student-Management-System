
import time
import matplotlib.pyplot as plt
import random

def randomized_partition(arr, low, high):
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

sizes = [10**4, 10**5, 10**6, 10**7]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = randomized_partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

merge_times = []
quick_times = []

for n in sizes:
    arr1 = list(range(n, 0, -1))
    arr2 = arr1.copy()

    start = time.perf_counter()
    merge_sort(arr1)
    end = time.perf_counter()
    merge_times.append(end - start)

    start = time.perf_counter()
    quick_sort(arr2, 0, n - 1)
    end = time.perf_counter()
    quick_times.append(end - start)

plt.figure(figsize=(10, 6))
plt.plot(sizes, merge_times, marker='o', label="Merge Sort")
plt.plot(sizes, quick_times, marker='s', label="Quick Sort")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.title("Merge Sort vs Quick Sort (Time Complexity Analysis)")
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.show()
