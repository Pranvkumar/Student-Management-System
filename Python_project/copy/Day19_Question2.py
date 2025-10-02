def find_peak_element(nums):
    # Finds any peak element's index in the array using binary search.
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left

# Example usage:
if __name__ == "__main__":
    # Problem 2
    print(find_peak_element([1, 3, 20, 4, 1, 0]))  
    print(find_peak_element([1, 2, 1, 3, 5, 6, 4])) 
    print(find_peak_element([10, 20, 15, 2, 23, 90, 67]))  