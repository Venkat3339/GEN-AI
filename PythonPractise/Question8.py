# Write a program to find the greatest common divisor (GCD) of two numbers without using the math library, using a while loop.

# Input reading
first = int(input("Enter a number: "))
second = int(input("Enter a number: "))
lower = min(first,second) # gives smallest value of first and second
# Loop that gives the GCD of two numbers
for i in range(1,lower+1):
    if((first % i == 0) and (second % i == 0)):
        GCD = i
# Printing greatest common divisor of two numbers
print("The greatest common divisor of two numbers: ", GCD)