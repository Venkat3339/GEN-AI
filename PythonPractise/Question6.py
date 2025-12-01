# Write a while loop program that keeps asking the user to enter a positive number and stops only when the user enters a negative number.

# loop that keeps asking the user to enter a positive number and stops only when the user enters a negative number
while(True):
    number = int(input("Enter a Number: "))
    if( number < 0):
        break