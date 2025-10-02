# Day 18 - Sorting Algorithms
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Example usage:
if __name__ == "__main__":
    # Selection Sort
    print(selection_sort([29, 10, 14, 37, 13]))
    print(selection_sort([64, 25, 12, 22, 11]))  
    print(selection_sort([5, 3, 8, 1, 6]))       