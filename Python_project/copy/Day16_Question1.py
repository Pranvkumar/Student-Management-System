def linear_search(arr, target):
# Searches for the target element in the array using linear search.
# Returns the index if found, else returns -1.
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

# Example usage:
if __name__ == "__main__":
    # Linear Search Examples
    result1 = linear_search([10, 20, 30, 40, 50], 30)
    print(f"Index of 30: {result1}") 

    result2 = linear_search([1, 5, 9, 3, 7], 8)
    print(f"Index of 8: {result2}")  

    result3 = linear_search([15, 25, 35, 45], 25)
    print(f"Index of 25: {result3}")