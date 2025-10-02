# Day 17 - Binary Search Problems
# 3. Integer Square Root Using Binary Search
def integer_sqrt(n):
    if n < 0:
        raise ValueError("Input must be non-negative")
    if n == 0 or n == 1:
        return n
    left, right = 1, n
    ans = 1
    while left <= right:
        mid = (left + right) // 2
        if mid * mid == n:
            return mid
        elif mid * mid < n:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1
    return ans

# Example usage:
if __name__ == "__main__":
    # 3. Integer Square Root
    print(integer_sqrt(16))                              # Output: 4
    print(integer_sqrt(27))                              # Output: 5
    print(integer_sqrt(49))                              # Output: 7