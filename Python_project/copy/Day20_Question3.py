import heapq
# 3. Kth Largest Element (using heapq.nlargest for efficiency)
def kth_largest_element(arr, k):
    # Finds the Kth largest element in an unsorted array.
    return heapq.nlargest(k, arr)[-1]

# Example usage:
if __name__ == "__main__":
    # 3. Kth Largest Element
    print(kth_largest_element([3, 2, 1, 5, 6, 4], 2))  
    print(kth_largest_element([7, 10, 4, 3, 20, 15], 3)) 
    print(kth_largest_element([1, 23, 12, 9, 30, 2, 50], 4)) 