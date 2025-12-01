# Develop a program that checks whether an input number is a palindrome using loops and conditional statements.

# A function that returns the number is palindrome or not
def reverseOfNumber(n):
    temparary = n
    reverseOfNumber = 0
    # Loop that gives the reverse of a number
    while(n!=0):
        temp = n%10
        reverseOfNumber = ( reverseOfNumber * 10 ) + temp 
        n //=10
    return temparary == reverseOfNumber

# Main
# input Reading
number = int(input("Enter a number: "))
# If-else block to decide the number is palindrome or not 
if(reverseOfNumber(number)):
    print("The given number is palindrome: ",number)
else:
    print("The given number is not a palindrome: ",number)