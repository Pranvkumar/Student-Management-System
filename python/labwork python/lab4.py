# Lab 4: Demonstrating the concept of List & Tuple

# 1. Create the list through different ways, and display the list content
# Directly
list1 = [1, 2, 3, 4, 5]
print("List1:", list1)
# Through loop
list2 = []
for i in range(6, 11):
    list2.append(i)
print("List2:", list2)
# Slicing
print("Sliced List1 (2-4):", list1[1:4])

# 2. Do the list cloning
list3 = list1[:]
print("Cloned List3 from List1:", list3)
list4 = list1.copy()
print("Cloned List4 from List1 using copy():", list4)

# 3. Show the list processing through various functions
list1.append(6)
print("After append:", list1)
list1.insert(0, 0)
print("After insert:", list1)
list1.extend([7, 8, 9])
print("After extend:", list1)
print("Count of 3 in List1:", list1.count(3))
list1.remove(3)
print("After remove 3:", list1)
popped_element = list1.pop()
print("After pop:", list1, "Popped element:", popped_element)
list1.sort()
print("After sort:", list1)
print("Max element in List1:", max(list1))
print("Min element in List1:", min(list1))

# 4. Find the common elements between two lists
list4 = [4, 5, 6, 7, 8]
common_elements = list(set(list1) & set(list4))
print("Common elements between List1 and List4:", common_elements)

def modify_list(lst):
    lst.append(10)
    print("Inside function, modified list:", lst)
modify_list(list1)
print("Outside function, modified list:", list1)


# Creating tuples
tuple1 = (1, 2, 3, 4, 5)
print("Tuple1:", tuple1)
tuple2 = tuple(range(6, 11))
print("Tuple2:", tuple2)

# Slicing
print("Sliced Tuple1 (2-4):", tuple1[1:4])

tuple3 = tuple1[:]
print("Cloned Tuple3 from Tuple1:", tuple3)

# Finding common elements between two tuples
tuple4 = (4, 5, 6, 7, 8)
common_elements_tuple = tuple(set(tuple1) & set(tuple4))
print("Common elements between Tuple1 and Tuple4:", common_elements_tuple)

# Tuples are immutable, so we cannot show mutable property through function
def try_modify_tuple(tpl):
    try:
        tpl += (10,)
        print("Inside function, modified tuple:", tpl)
    except TypeError as e:
        print("Error:", e)

try_modify_tuple(tuple1)
print("Outside function, original tuple:", tuple1)