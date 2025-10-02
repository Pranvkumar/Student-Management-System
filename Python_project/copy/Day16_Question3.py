def find_maximum(arr):
# Finds and returns the largest element in the array.
    if not arr:
        raise ValueError("Array is empty")
    max_val = arr[0]
    for val in arr[1:]:
        if val > max_val:
            max_val = val
    return max_val

# Example usage:
if __name__ == "__main__":
    # Find Maximum Element Examples
    print(find_maximum([3, 7, 1, 9, 4, 6]))                # Output: 9
    print(find_maximum([-5, -2, -8, -1, -3]))              # Output: -1
    print(find_maximum([100, 250, 75, 300, 150]))          # Output: 300