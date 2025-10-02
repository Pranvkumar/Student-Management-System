# Day 18 - Sorting Algorithms
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

# Example usage:
if __name__ == "__main__":
    # Insertion Sort
    print(insertion_sort([12, 11, 13, 5, 6]))    
    print(insertion_sort([31, 41, 59, 26, 53]))  
    print(insertion_sort([4, 2, 7, 1, 3]))      