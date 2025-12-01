# Using a for loop, generate a list of squares of only the odd numbers from 1 to 20.

# Main
start = int(input("Enter a Number: "))
end = int(input("Enter a Number: "))
squaresOfOddNumbers = []
#Loop that gives the squares of odd numbers in given range
for i in range(start, end+1):
    if(i%2!=0):
        odd = i**2
        squaresOfOddNumbers.append(odd)
# Printing collected squares of odd numbers
print("Squares of odd numbers: ",squaresOfOddNumbers)