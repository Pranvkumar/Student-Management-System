def count_occurrences(arr, target):
# Counts how many times the target appears in the array.
    count = 0
    for val in arr:
        if val == target:
            count += 1
    return count


# Example usage:
if __name__ == "__main__":
    # Count Occurrences Examples
    print(count_occurrences([1, 2, 3, 2, 2, 4], 2))         # Output: 3
    print(count_occurrences([5, 1, 5, 5, 3, 5, 7], 5))      # Output: 4
    print(count_occurrences([10, 20, 30, 10, 40], 10))      # Output: 2