#include <stdio.h>
#include <stdlib.h>

// Iterative Merge function (same as recursive version)
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    int L[n1], R[n2];
    
    // Copy data to temp arrays
    for (int i = 0; i < n1; i++) 
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) 
        R[j] = arr[m + 1 + j];
    
    // Merge the temp arrays back into arr[l..r]
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) 
            arr[k++] = L[i++];
        else 
            arr[k++] = R[j++];
    }
    
    // Copy remaining elements
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

// Iterative Merge Sort using bottom-up approach
void mergeSortIterative(int arr[], int n) {
    int curr_size;  // Current size of subarrays to be merged
    int left_start; // Starting point of left sub array
    
    // Merge subarrays in bottom up manner
    // First merge subarrays of size 1 to create sorted subarrays of size 2
    // Then merge subarrays of size 2 to create sorted subarrays of size 4, and so on.
    for (curr_size = 1; curr_size <= n - 1; curr_size = 2 * curr_size) {
        // Pick starting point of different subarrays of current size
        for (left_start = 0; left_start < n - 1; left_start += 2 * curr_size) {
            // Calculate mid point to break the sub array in two halves
            int mid = left_start + curr_size - 1;
            
            // Calculate end point of right sub array
            int right_end = (left_start + 2 * curr_size - 1 < n - 1) ? 
                           left_start + 2 * curr_size - 1 : n - 1;
            
            // Merge subarrays if mid is smaller than right_end
            if (mid < right_end)
                merge(arr, left_start, mid, right_end);
        }
    }
}

// Iterative Binary Search
int binarySearchIterative(int arr[], int n, int x) {
    int left = 0, right = n - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        // If x is found at mid, return 1 (found)
        if (arr[mid] == x)
            return mid;
        
        // If x is greater, ignore left half
        if (arr[mid] < x)
            left = mid + 1;
        // If x is smaller, ignore right half
        else
            right = mid - 1;
    }
    
    // Element not found
    return -1;
}

// Function to print array
void printArray(int arr[], int n) {
    printf("Sorted array: ");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int n, x;
    
    printf("Enter the number of elements: ");
    scanf("%d", &n);
    
    int arr[n];
    printf("Enter %d elements: ", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    
    printf("Enter the element to search: ");
    scanf("%d", &x);
    
    printf("Original array: ");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
    
    // Sort the array using iterative merge sort
    mergeSortIterative(arr, n);
    
    // Print sorted array
    printArray(arr, n);
    
    // Search for element using iterative binary search
    int idx = binarySearchIterative(arr, n, x);
    if (idx != -1)
        printf("Element %d: Found at index %d\n", x, idx);
    else
        printf("Element %d: Not Found\n", x);
    
    return 0;
}