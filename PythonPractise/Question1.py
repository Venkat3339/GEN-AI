# Write a Python program to print all prime numbers between 10 and 100 using a for loop and if conditions.

# import statement
import math
# Prime Function
# This function Will give the given number is prime or not 
def isPrime(n):
    count = 0
    rear = int(math.sqrt(n))+1
    # Loop starts from 2 since one can divide all the numbers 
    for i in range(2, rear):
        if( n%i == 0 ):
            count += 1
    return count == 0 and n!=1

# Main
# Input reading
start = int(input("Enter a Number: "))
end = int(input("Enter a Number: "))
primeCollection = []
# Loop that collects all prime numbers to a list 
for i in range(start,end+1):
    if(isPrime(i)):
        primeCollection.append(i)
# Printing prime collection
print("The prime Numbers are: ", primeCollection)