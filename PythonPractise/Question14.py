# Using logical operators, write a program that accepts a user’s age and salary and determines if they are eligible for a loan (age ≥ 21 and salary ≥ ₹25,000).

# Input reading
age = int(input("Enter a number: "))
salary = float(input("Enter a number: "))

# If-else block to know the person is eligible for the loan or not
if(age >= 21 and salary >= 25000):
    print("The person is eligible to take the loan")
else:
    print("The person is not eligible to take the loan")
