# Corrected Version of Binary Search
def binary_search_correct(nums, target):
    """
    Corrected Binary Search:
    - Sets right = len(nums) - 1 to stay within valid index range
    - Uses left <= right to ensure all elements are checked
    - Updates left = mid + 1 and right = mid - 1 correctly to move bounds
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1  # Move to upper half
        else:
            right = mid - 1  # Move to lower half
    return -1

# 🧪 Test Cases
arr = [1, 3, 5, 7, 9, 11]
target = 7

# Test correct version (should return index 3)
result_correct = binary_search_correct(arr, target)
print("Correct Binary Search Result:", result_correct)