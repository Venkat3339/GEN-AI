# Write a Python program that reads 5 names from the user and stores only the names that start with a vowel into a new list.

Names = []
vowels = 'aeiouAEIOU'
newListOfNames = []
# Loop to read the five names
for i in range(5):
    Name = input("Enter the name: ")
    Names.append(Name)
# Loop that gives the list of names that starts with vowel 
for i in Names:
    firstLetter = i[0]
    if(firstLetter in vowels):
        newListOfNames.append(i)
# Printing list of names that start with vowel
print("Names that start with vowels: ",newListOfNames)
