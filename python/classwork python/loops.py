#while loop and break
# num=int(input("Enter the number loop : "))
# i=0
# while(i<num):
#     if (i==3):
#         print(i)
#         break
#     print(i)
#     i+=1
# print("End")

#continue and while loop
# num=int(input("Enter the number loop : "))
# i=0
# while(i<num):
#     num-=1
#     if (num%2==0):
#         continue
#     print(num)
   
# print("End")

#Infinite loop
# while (1):
#     print("This is infinite loop")

# num =int(input("Enter the number : "))
# for i in range(1,11):
#  c =num*i
#  print(num,"*",i,"=",c)

# n=int(input("Enter the number : "))
# for i in range(2,n,2):
#     print(i)

#Hello name function
# lists = ['Pranvkumar','Ranjan','Ashutosh','Devansh']
# for i in range(len(lists)):
#     print("Hello",lists[i])

#Program to number pyramid
# rows = int(input("Enter the rows :"))
# for i in range(1,rows+1):
#     for j in range(i):
#         print(i,end = ' ')
#     print()

#Program to reverse number pyramid
# rows = int(input("Enter the rows :"))
# for i in range(rows,0,-1):
#     for j in range(i):
#         print(i, end=' ')
#     print()


# rows = int(input("Enter the rows :"))
# for i in range(1, rows + 1):
#     for k in range(rows - i):
#         print(" ", end='')
#     for j in range(i):
#         print(i, " ", end='')
#     print()

# Example of pass statement
# for i in range(10):
#     if i == 5:
#         pass 
#     else:
#         print(i)