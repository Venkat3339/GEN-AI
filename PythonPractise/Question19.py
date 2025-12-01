# Write a script that opens a file named data.txt, reads its numbers, and prints the sum of only even numbers found in the file.

# File opening in read mode
file = open('C:\\pyrhon\\Practice Questions\\test1.txt', 'r')
even = 0
line = str(file.readline())
storeTOList = (line.split(' ')) # storing the numbers of string to list separeted by space
# Loop to get sum of odd and even numbers
for i in storeTOList:
    if( int(i) % 2 == 0 ):
        even+=int(i)
# Printing the values
print("Even number count: ", even) 
# File closing  
file.close()


