import numpy as np
import time
import matplotlib.pyplot as plt

def traditional_multiply(A, B):
    n = len(A)
    C = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def split(matrix):
    n = len(matrix)
    mid = n // 2
    return matrix[:mid, :mid], matrix[:mid, mid:], matrix[mid:, :mid], matrix[mid:, mid:]

def divide_and_conquer_multiply(A, B):
    n = len(A)
    if n == 1:
        return A * B
    
    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)
    
    C11 = divide_and_conquer_multiply(A11, B11) + divide_and_conquer_multiply(A12, B21)
    C12 = divide_and_conquer_multiply(A11, B12) + divide_and_conquer_multiply(A12, B22)
    C21 = divide_and_conquer_multiply(A21, B11) + divide_and_conquer_multiply(A22, B21)
    C22 = divide_and_conquer_multiply(A21, B12) + divide_and_conquer_multiply(A22, B22)
    
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C

def strassen_multiply(A, B):
    n = len(A)
    # For smaller matrices, the overhead of Strassen's makes it slower.
    # A threshold of 16 or 32 is common.
    if n <= 16: 
        return traditional_multiply(A, B)

    # Pad the matrix to the next power of 2 if it's not already
    if n & (n - 1) != 0:
        next_power_of_2 = 1 << (n - 1).bit_length()
        padded_A = np.zeros((next_power_of_2, next_power_of_2))
        padded_B = np.zeros((next_power_of_2, next_power_of_2))
        padded_A[:n, :n] = A
        padded_B[:n, :n] = B
        result = strassen_multiply(padded_A, padded_B)
        return result[:n, :n] # Unpad the result

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    P1 = strassen_multiply(A11, B12 - B22)
    P2 = strassen_multiply(A11 + A12, B22)
    P3 = strassen_multiply(A21 + A22, B11)
    P4 = strassen_multiply(A22, B21 - B11)
    P5 = strassen_multiply(A11 + A22, B11 + B22)
    P6 = strassen_multiply(A12 - A22, B21 + B22)
    P7 = strassen_multiply(A11 - A21, B11 + B12)

    C11 = P5 + P4 - P2 + P6
    C12 = P1 + P2
    C21 = P3 + P4
    C22 = P5 + P1 - P3 - P7

    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C

def main():
    sizes = [ 128 , 256, 512]  # Reduced sizes for practical execution time
    times_traditional = []
    times_divide_conquer = []
    times_strassen = []

    for n in sizes:
        A = np.random.randint(0, 10, size=(n, n))
        B = np.random.randint(0, 10, size=(n, n))

        start_time = time.time()
        traditional_multiply(A, B)
        end_time = time.time()
        times_traditional.append(end_time - start_time)

        start_time = time.time()
        divide_and_conquer_multiply(A, B)
        end_time = time.time()
        times_divide_conquer.append(end_time - start_time)

        start_time = time.time()
        strassen_multiply(A, B)
        end_time = time.time()
        times_strassen.append(end_time - start_time)

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_traditional, 'o-', label='Traditional O(n^3)')
    plt.plot(sizes, times_divide_conquer, 's-', label='Divide and Conquer O(n^3)')
    plt.plot(sizes, times_strassen, '^-', label="Strassen's O(n^2.81)")
    
    plt.title('Matrix Multiplication Performance Comparison')
    plt.xlabel('Matrix Size (n x n)')
    plt.ylabel('Execution Time (seconds)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
