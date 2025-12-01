# Write a Python program that checks if a number is divisible by both 3 and 5, but not by 7.

# Input reading
number = int(input("Enter a number: "))
# If-else block that says pass or fail based on the condition A number divisible by both 3 and 5 but not by 7
if(number % 3 == 0 and number % 5 == 0 and number % 7 != 0):
    print("Pass")
else:
    print("Fail")