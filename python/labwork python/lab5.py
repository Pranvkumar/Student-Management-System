squares = [i**2 for i in range(1, 51)]
print("Squares from 1 to 50:", squares)
print("\n")

def count_characters(s):
    count = 0
    for char in s:
        count += 1
    return count
string = "Name is pranvkumar suhas kshirsagar"
print(f"Number of characters in '{string}':", count_characters(string))
print("\n")

def reverse_string(s):
    reversed = ""
    for char in s:
        reversed = char + reversed
    return reversed
string = "string is name so pranvkumar"
print(f"Reversed string of '{string}':", reverse_string(string))
print("This is also string reversed :",string[::-1])
print("\n")

def is_prime(n):
    if n <= 1:
        return False
    if n % 2 == 0:
        return n == 2
    for i in range(3, n, 2):
        if n % i == 0:
            return False
    return True
primes = [i for i in range(2, 50) if is_prime(i)]
print("Prime numbers below 50:", primes)
print("\n")

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return n == sum(d**3 for d in digits)

armstrong_numbers = [i for i in range(1, 1001) if is_armstrong(i)]
print("Armstrong numbers from 1 to 1000:", armstrong_numbers)