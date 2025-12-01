# Write a Python script to count how many vowels are present in a given string without using built-in count functions.

# Reading the input
String = input("Enter the String: ")
count = 0
vowels = 'aeiouAEIOU'
# Loop that returns the count of vowels in a string 
for i in String:
    if( i in vowels ):
        count += 1
# Printing the count of vowels
print(count)