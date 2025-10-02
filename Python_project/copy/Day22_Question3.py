class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def print_linked_list(head):
    current = head
    while current:
        print(current.data, end=" ")
        current = current.next
    print()

def create_linked_list(values):
    head = Node(values[0])
    current = head
    for val in values[1:]:
        current.next = Node(val)
        current = current.next
    return head

# Example usage:
list1 = create_linked_list([1, 2])
print_linked_list(list1)

list2 = create_linked_list([49, 10, 30])
print_linked_list(list2)  