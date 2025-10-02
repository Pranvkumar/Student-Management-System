def add_pair(dictionary):
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    dictionary[name] = age

def delete_pair(dictionary):
    name = input("Enter name to delete: ")
    if name in dictionary:
        del dictionary[name]
    else:
        print("Name not found!")

def update_age(dictionary):
    name = input("Enter name to update age: ")
    if name in dictionary:
        age = int(input("Enter new age: "))
        dictionary[name] = age
    else:
        print("Name not found!")

def display_count(dictionary):
    print(f"Total pairs: {len(dictionary)}")

def display_age(dictionary):
    name = input("Enter name to get age: ")
    if name in dictionary:
        print(f"Age of {name} is {dictionary[name]}")
    else:
        print("Name not found!")

def main():
    dictionary = {}
    num_pairs = int(input("How many pairs of name and age do you want to add? "))
    
    for _ in range(num_pairs):
        add_pair(dictionary)
    
    print("\nDisplaying all pairs:")
    for name, age in dictionary.items():
        print(f"Name: {name}, Age: {age}")
    
    add_pair(dictionary)
    delete_pair(dictionary)
    update_age(dictionary)
    display_count(dictionary)
    display_age(dictionary)
    
    clone_dict = dictionary.copy()
    print(f"Original dictionary id: {id(dictionary)}")
    print(f"Cloned dictionary id: {id(clone_dict)}")
    
    list1 = ['name1', 'name2', 'name3']
    list2 = [21, 22, 23]
    zipped_dict = dict(zip(list1, list2))
    print(f"Dictionary from lists: {zipped_dict}")
    
    string = "name1:21,name2:22,name3:23"
    string_dict = dict(item.split(":") for item in string.split(","))
    print(f"Dictionary from string: {string_dict}")

if __name__ == "__main__":
    main()