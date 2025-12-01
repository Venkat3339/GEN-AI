# Create a program that counts how many lines, words, and characters exist in a text file.

# File reading
file = open('C:\\pyrhon\\Practice Questions\\test.txt', 'r')
numberOfLines = 0
numberOfWords = 0
numberOfCharacters = 0

# Loop to iterate the file
for i in file:
    tempList = []
    numberOfLines += 1
    tempList.append(i.split(' ')) # adding the space separeted word into list
    # Loop to count the number of words
    for k in tempList:
        numberOfWords += len(k)
    # Loop to count the number of Characters
    for j in i:
        if(j != ' '):
            numberOfCharacters+=1
# Printing the values
print("The number of lines in the file", numberOfLines)
print("The number of words in the file", numberOfWords)
print("The number of characters in the file", numberOfCharacters)
# File closing
file.close()
