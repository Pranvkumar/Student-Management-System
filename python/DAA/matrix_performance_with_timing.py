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


# Start tracking total runtime
total_start_time = time.time()

sizes = [256, 512, 1024]  # larger matrices
time_trad, time_div, time_strassen = [], [], []

print("=== Matrix Multiplication Performance Comparison ===")
print(f"Testing matrix sizes: {sizes}")
print()

for n in sizes:
    print(f"Running for size: {n}x{n} ...")
    A = np.random.randint(1, 10, (n, n))
    B = np.random.randint(1, 10, (n, n))
    
    # Traditional
    print("  - Traditional method...", end=" ")
    start = time.time()
    multiply_traditional(A, B)
    trad_time = time.time() - start
    time_trad.append(trad_time)
    print(f"{trad_time:.3f}s")
    
    # Divide & Conquer
    print("  - Divide & Conquer method...", end=" ")
    start = time.time()
    multiply_divide_conquer(A, B)
    div_time = time.time() - start
    time_div.append(div_time)
    print(f"{div_time:.3f}s")
    
    # Strassen
    print("  - Strassen method...", end=" ")
    start = time.time()
    strassen(A, B)
    strassen_time = time.time() - start
    time_strassen.append(strassen_time)
    print(f"{strassen_time:.3f}s")
    
    print()

# Calculate total runtime
total_end_time = time.time()
total_runtime = total_end_time - total_start_time

# Display results summary
print("=== RESULTS SUMMARY ===")
print()
for i, n in enumerate(sizes):
    print(f"Matrix Size {n}x{n}:")
    print(f"  Traditional:     {time_trad[i]:.3f}s")
    print(f"  Divide & Conquer: {time_div[i]:.3f}s")
    print(f"  Strassen:        {time_strassen[i]:.3f}s")
    print()

print("=== TIMING BREAKDOWN ===")
print(f"Total algorithm execution time: {sum(time_trad) + sum(time_div) + sum(time_strassen):.3f}s")
print(f"  - Traditional total:     {sum(time_trad):.3f}s")
print(f"  - Divide & Conquer total: {sum(time_div):.3f}s")
print(f"  - Strassen total:        {sum(time_strassen):.3f}s")
print()
print(f"TOTAL PROGRAM RUNTIME: {total_runtime:.3f}s")
print(f"(includes matrix generation, plotting, and overhead)")
print()

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

print("=== ANALYSIS ===")
print("Fastest algorithm for each matrix size:")
for i, n in enumerate(sizes):
    times = [time_trad[i], time_div[i], time_strassen[i]]
    methods = ["Traditional", "Divide & Conquer", "Strassen"]
    fastest_idx = times.index(min(times))
    print(f"  {n}x{n}: {methods[fastest_idx]} ({times[fastest_idx]:.3f}s)")