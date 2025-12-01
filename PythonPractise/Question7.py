# Using a while loop, reverse the digits of a given integer (e.g., 12345 → 54321).

# input Reading
number = int(input("Enter a number: "))
reverseOfNumber = 0
# Loop that gives the reverse of a number
while(number!=0):
    temp = number%10
    reverseOfNumber = ( reverseOfNumber * 10 ) + temp 
    number //=10
# Printing reverse of a given number
print("Reverse of a given number: ",reverseOfNumber)

# Without while loop

number = int(input("Enter a number: "))
temp = str(number)
reverseOfNumber = int(temp[::-1])
# Printing reverse of a given number
print("Reverse of a given number: ",reverseOfNumber)
