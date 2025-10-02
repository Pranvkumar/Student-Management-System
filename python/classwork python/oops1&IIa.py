from abc import ABC, abstractmethod
# Example of a Class and Object
class College:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def get_details(self):
        return f"{self.name} is located in {self.location}"

# Creating an object of the College class
college1 = College("XYZ College", "Mumbai")
print(college1.get_details())

# Example of Inheritance
class Student(College):
    def __init__(self, name, age, college_name, college_location):
        super().__init__(college_name, college_location)
        self.name = name
        self.age = age

    def get_details(self):
        return f"{self.name}, aged {self.age}, studies at {self.name} located in {self.location}"

# Creating an object of the Student class
student1 = Student("Pranvkumar", 20, "XYZ College", "Mumbai")
print(student1.get_details())

class Professor(College):
    def __init__(self, name, department, college_name, college_location):
        super().__init__(college_name, college_location)
        self.name = name
        self.department = department

    def get_details(self):
        return f"Professor {self.name} from {self.department} department teaches at {self.name} located in {self.location}"

# Creating an object of the Professor class
professor1 = Professor("Dr. None", "Computer Science", "XYZ College", "Mumbai")
print(professor1.get_details())

# Example of Polymorphism
class Staff(College):
    def __init__(self, name, role, college_name, college_location):
        super().__init__(college_name, college_location)
        self.name = name
        self.role = role

    def get_details(self):
        return f"Staff member {self.name} works as {self.role} at {self.name} located in {self.location}"

class Visitor:
    def __init__(self, name):
        self.name = name

    def get_details(self):
        return f"Visitor {self.name} is visiting the college"

# Using polymorphism
def print_details(person):
    print(person.get_details())

staff = Staff("Anita", "Librarian", "XYZ College", "Mumbai")
visitor = Visitor("Mr. Sharma")

print_details(student1)
print_details(professor1)
print_details(staff)
print_details(visitor)

# Example of Abstraction
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

# Creating an object of the Circle class
circle = Circle(5)
print("Area of circle:", circle.area()) 

class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def display(self):
        print("ID:", self.id, "Name:", self.name)

emp1 = Employee("Gagan", 101)
emp1.display()  

class Student:
    school = "ABC School"

    def __init__(self, name, age):
        self.name = name  
        self.age = age

    def display(self):
        print("Name:", self.name, "Age:", self.age, "School:", self.school)

s1 = Student("Amit", 22)
s2 = Student("Rahul", 23)

s1.display()  
s2.display()  

class Student:
    def __init__(self, name, id, age):
        self.name = name
        self.id = id
        self.age = age

s = Student("Amit", 101, 22)

print(getattr(s, 'name'))
setattr(s, "age", 23)
print(getattr(s, 'age'))
print(hasattr(s, 'id'))  
delattr(s, 'age')

class Student:
    """This is a Student class."""
    def __init__(self, name, id, age):
        self.name = name
        self.id = id
        self.age = age

s = Student("Amit", 101, 22)
print(s.__doc__) 
print(s.__dict__)  
print(s.__module__) 

class Student:
    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id

    def display(self):
        print("Name:", self.name, "ID:", self.id)

s1 = Student()  
s1.display()  

s2 = Student("Amit", 101)  
s2.display()  

class Student:
    count = 0

    def __init__(self):
        Student.count += 1

s1 = Student()
s2 = Student()
s3 = Student()

print("Number of students:", Student.count)
# Example of Multiple Inheritance
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_person_details(self):
        return f"Name: {self.name}, Age: {self.age}"

class Employee:
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def get_employee_details(self):
        return f"Employee ID: {self.employee_id}"

class Manager(Person, Employee):
    def __init__(self, name, age, employee_id, department):
        Person.__init__(self, name, age)
        Employee.__init__(self, employee_id)
        self.department = department

    def get_details(self):
        return f"{self.get_person_details()}, Employee ID: {self.employee_id}, Department: {self.department}"

# Creating an object of the Manager class
manager1 = Manager("Amit", 35, "M123", "HR")
print(manager1.get_details())
