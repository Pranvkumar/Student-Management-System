# Day 15 - Sorting Problems
# 3. Bubble Sort Implementation
def bubble_sort(arr):
#Sorts an array of integers in ascending order using bubble sort algorithm.
    n = len(arr)
    result = arr.copy()
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result

# Example:
if __name__ == "__main__":
    # 3. Bubble Sort Implementation
    print(bubble_sort([5, 2, 8, 1, 9]))
    print(bubble_sort([3, 7, 4, 1, 6, 2]))
    print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))