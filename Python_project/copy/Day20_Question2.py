# 2. Merge Two Sorted Arrays
def merge_sorted_arrays(arr1, arr2):
    # Merges two sorted arrays into a single sorted array.
    merged = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1
    # Append remaining elements
    merged.extend(arr1[i:])
    merged.extend(arr2[j:])
    return merged

# Example usage:
if __name__ == "__main__":
    # 2. Merge Two Sorted Arrays
    print(merge_sorted_arrays([1, 3, 5], [2, 4, 6])) 
    print(merge_sorted_arrays([1, 5, 9, 10], [2, 3, 8, 13])) 
    print(merge_sorted_arrays([10, 30, 50], [20, 40, 60, 70])) 