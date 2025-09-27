import numpy as np
import time
import matplotlib.pyplot as plt


def multiply_traditional(A, B):
    n = len(A)
    C = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def multiply_divide_conquer(A, B):
    n = len(A)
    if n == 1:
        return A * B
    
    k = n // 2
    A11, A12, A21, A22 = A[:k,:k], A[:k,k:], A[k:,:k], A[k:,k:]
    B11, B12, B21, B22 = B[:k,:k], B[:k,k:], B[k:,:k], B[k:,k:]
    
    C11 = multiply_divide_conquer(A11, B11) + multiply_divide_conquer(A12, B21)
    C12 = multiply_divide_conquer(A11, B12) + multiply_divide_conquer(A12, B22)
    C21 = multiply_divide_conquer(A21, B11) + multiply_divide_conquer(A22, B21)
    C22 = multiply_divide_conquer(A21, B12) + multiply_divide_conquer(A22, B22)
    
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    return np.vstack((top, bottom))

def strassen(A, B):
    n = len(A)
    if n == 1:
        return A * B
    
    k = n // 2
    A11, A12, A21, A22 = A[:k,:k], A[:k,k:], A[k:,:k], A[k:,k:]
    B11, B12, B21, B22 = B[:k,:k], B[:k,k:], B[k:,:k], B[k:,k:]
    
    M1 = strassen(A11 + A22, B11 + B22)
    M2 = strassen(A21 + A22, B11)
    M3 = strassen(A11, B12 - B22)
    M4 = strassen(A22, B21 - B11)
    M5 = strassen(A11 + A12, B22)
    M6 = strassen(A21 - A11, B11 + B12)
    M7 = strassen(A12 - A22, B21 + B22)
    
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    return np.vstack((top, bottom))


sizes = [256,512,1024]  # larger matrices
time_trad, time_div, time_strassen = [], [], []

for n in sizes:
    print(f"Running for size: {n}x{n} ...")
    A = np.random.randint(1, 10, (n, n))
    B = np.random.randint(1, 10, (n, n))
    
    # Traditional
    start = time.time()
    multiply_traditional(A, B)
    time_trad.append(time.time() - start)
    
    # Divide & Conquer
    start = time.time()
    multiply_divide_conquer(A, B)
    time_div.append(time.time() - start)
    
    # Strassen
    start = time.time()
    strassen(A, B)
    time_strassen.append(time.time() - start)


plt.figure(figsize=(8,6))
plt.plot(sizes, time_trad, 'o-', label="Traditional")
plt.plot(sizes, time_div, 's-', label="Divide & Conquer")
plt.plot(sizes, time_strassen, '^-', label="Strassen")
plt.xlabel("Matrix Size (n x n)")
plt.ylabel("Execution Time (seconds)")
plt.title("Performance Comparison: Traditional vs Divide & Conquer vs Strassen")
plt.legend()
plt.grid(True)
plt.show()
