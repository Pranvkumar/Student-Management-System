class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow.data  # slow points to the middle

# Example usage:
def create_linked_list(values):
    head = Node(values[0])
    current = head
    for val in values[1:]:
        current.next = Node(val)
        current = current.next
    return head

list1 = create_linked_list([1, 2, 3, 4, 5])
print("Middle:", find_middle(list1)) 

list2 = create_linked_list([2, 4, 6, 7, 5, 1])
print("Middle:", find_middle(list2))  
