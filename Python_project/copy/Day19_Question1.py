def search_in_rotated_array(nums, target):
    # Searches for target in a rotated sorted array and returns its index, or -1 if not found.
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1

# Example usage:
if __name__ == "__main__":
    # Problem 1
    print(search_in_rotated_array([4, 5, 6, 7, 0, 1, 2], 0))
    print(search_in_rotated_array([4, 5, 6, 7, 0, 1, 2], 3))  
    print(search_in_rotated_array([11, 13, 15, 17, 19, 2, 3, 6, 7], 6))  