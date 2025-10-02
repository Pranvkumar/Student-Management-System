class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def count_frequency(head, key):
    count = 0
    current = head
    while current:
        if current.data == key:
            count += 1
        current = current.next
    return count

def create_linked_list(values):
    head = Node(values[0])
    current = head
    for val in values[1:]:
        current.next = Node(val)
        current = current.next
    return head

# Example usage:
list1 = create_linked_list([1, 2, 1, 2, 1, 3, 1])
print("Frequency of 1:", count_frequency(list1, 1))  

list2 = create_linked_list([1, 2, 1, 2, 1])
print("Frequency of 3:", count_frequency(list2, 3))  