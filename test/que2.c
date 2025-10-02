#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void insert(struct Node **head)
{
    int data;
    printf("Enter the data : ");
    scanf("%d", &data);
    struct Node *newNode = createNode(data);
    if (newNode == NULL)
    {
        return;
    }

    if (*head == NULL)
    {
        newNode->next = newNode;
        *head = newNode;
        return;
    }

    struct Node *temp = *head;
    while (temp->next != *head)
    {
        temp = temp->next;
    }

    newNode->next = *head;
    temp->next = newNode;
    *head = newNode;
}


void findMiddle(struct Node* head) {
    struct Node *back = head, *front = head;

    if (head == NULL) {
        printf("The list is empty.\n");
        return;
    }

    do {
        front = front->next;
        if (front != head && front->next != head) {
            back = back->next;
            front = front->next;
        }
    } while (front != head && front->next != head);

    printf("The middle element is: %d\n", back->data);
}


void printList(struct Node* head) {
    if (head == NULL) {
        printf("The list is empty.\n");
        return;
    }

    struct Node* temp = head;
    do {
        printf("%d -> ", temp->data);
        temp = temp->next;
    } while (temp != head);
    printf("(back to head)\n");
}

int main()
{
    struct Node *head = NULL;
    int choice = 1;
    printList(head);

    do
    {
        insert(&head);
        printf("To exit enter 0 : ");
        scanf("%d",&choice);
        getchar();
    }
    while (choice != 0);
    printList(head);
    findMiddle(head);

    return 0;
}

