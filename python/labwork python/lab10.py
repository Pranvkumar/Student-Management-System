class ComplexNumber:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def printf(self):
        print(f"{self.real} + {self.imaginary}i")

    def add(self, other):
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)

    def subtract(self, other):
        return ComplexNumber(self.real - other.real, self.imaginary - other.imaginary)

    def multiply(self, other):
        real_part = self.real * other.real - self.imaginary * other.imaginary
        imaginary_part = self.real * other.imaginary + self.imaginary * other.real
        return ComplexNumber(real_part, imaginary_part)


real1 = float(input("Enter the real part of the first complex number: "))
imaginary1 = float(input("Enter the imaginary part of the first complex number: "))
complex1 = ComplexNumber(real1, imaginary1)

# complex2 = ComplexNumber(3, 4)
real2 = float(input("Enter the real part of the second complex number: "))
imaginary2 = float(input("Enter the imaginary part of the second complex number: "))
complex2 = ComplexNumber(real2, imaginary2)

print("First Complex Number:")
complex1.printf()
print("Second Complex Number:")
complex2.printf()

sum_result = complex1.add(complex2)
difference_result = complex1.subtract(complex2)
multiplication_result = complex1.multiply(complex2)

print("\nResults:")
print("Sum:")
sum_result.printf()
print("Difference:")
difference_result.printf()
print("Multiplication:")
multiplication_result.printf()