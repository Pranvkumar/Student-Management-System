class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        x, y = len(nums1), len(nums2)
        low, high = 0, x

        while low <= high:
            part1 = (low + high) // 2
            part2 = (x + y + 1) // 2 - part1

            maxX = float('-inf') if part1 == 0 else nums1[part1 - 1]
            minX = float('inf') if part1 == x else nums1[part1]

            maxY = float('-inf') if part2 == 0 else nums2[part2 - 1]
            minY = float('inf') if part2 == y else nums2[part2]

            if maxX <= minY and maxY <= minX:
                if (x + y) % 2 == 0:
                    return float((max(maxX, maxY) + min(minX, minY)) / 2)
                else:
                    return float(max(maxX, maxY))
                
            if float(maxX) > float(minY):
                high = part1 - 1
            else:
                low = part1 + 1

        raise ValueError("Input arrays are not sorted")

# Test case
solution = Solution()
nums1 = list(map(int, input("Enter the first sorted array (space-separated): ").split()))
nums2 = list(map(int, input("Enter the second sorted array (space-separated): ").split()))
result = solution.findMedianSortedArrays(nums1, nums2)
print(f"The median is: {result:.6f}")
