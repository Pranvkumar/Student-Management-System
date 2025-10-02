# Corrected Version of Dutch National Flag Algorithm
def sort_colors_correct(nums):
    """
    This version fixes the bug by not incrementing 'current' when a 2 is swapped in.
    We must re-check the swapped-in value at index 'current' before moving forward.
    """
    left, current, right = 0, 0, len(nums) - 1

    while current <= right:
        if nums[current] == 0:  # Red
            nums[left], nums[current] = nums[current], nums[left]
            left += 1
            current += 1  #  Safe: elements before 'left' are already sorted
        elif nums[current] == 1:  # White
            current += 1  #  Safe to skip 1
        else:  # Blue (nums[current] == 2)
            nums[current], nums[right] = nums[right], nums[current]
            right -= 1
            # Do NOT increment current here because the swapped-in element might be 0 or 2

    return nums

# 🧪 Test Case
input_array = [2, 0, 2, 1, 1, 0]
print("Original input:", input_array)

input_correct = input_array.copy()

print("Corrected Version Output :", sort_colors_correct(input_correct))  # Correct