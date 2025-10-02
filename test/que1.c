#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

struct stck {
    int data;
    struct stck* next;
};

struct stck* stcknode(int data) {
    struct stck* newNode = (struct stck*)malloc(sizeof(struct stck));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void push(struct stck** top, int data) {
    struct stck* newNode = stcknode(data);
    newNode->next = *top;
    *top = newNode;
}

int pop(struct stck** top) {
    if (*top == NULL) {
        printf("Stack underflow.\n");
        return -1;
    }
    struct stck* temp = *top;
    int popped = temp->data;
    *top = (*top)->next;
    free(temp);
    return popped;
}


void findSecondLargest(struct stck* top) {
    if (top == NULL || top->next == NULL) {
        printf("No elements.\n");
        return;
    }

    int largest, secondLargest;
    struct stck* temp = top;

    if (top->data > top->next->data) {
        largest = top->data;
        secondLargest = top->next->data;
    } else {
        largest = top->next->data;
        secondLargest = top->data;
    }

    temp = top->next->next; 

    while (temp != NULL) {
        if (temp->data > largest) {
            secondLargest = largest;
            largest = temp->data;
        } else if (temp->data > secondLargest && temp->data != largest) {
            secondLargest = temp->data;
        }
        temp = temp->next;
    }

    if (largest == secondLargest) {
        printf("No second largest element found.\n");
    } else {
        printf("The second largest element is: %d\n", secondLargest);
    }
}

void printStack(struct stck* top) {
    if (top == NULL) {
        printf("The stack is empty.\n");
        return;
    }

    struct stck* temp = top;
    printf("Stack elements: ");
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
    printf("\n");
}

int main() {
    struct stck* stack = NULL;
    int choice, data;

    do {
        printf("1. Push\n2. Pop\n3. Find Second Largest\n4. Print Stack\n0. Exit\nEnter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to push: ");
                scanf("%d", &data);
                push(&stack, data);
                break;
            case 2:
                data = pop(&stack);
                if (data != -1) {
                    printf("Popped: %d\n", data);
                }
                break;
            case 3:
                findSecondLargest(stack);
                break;
            case 4:
                printStack(stack);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice. Try again.\n");
        }
    } while (choice != 0);

    return 0;
}
