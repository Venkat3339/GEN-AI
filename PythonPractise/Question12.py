# Write a script to copy the contents of one text file into another, but exclude all lines that start with a “#” symbol.

# File opening in read mode
file = open('C:\\pyrhon\\Practice Questions\\test.txt', 'r')
# File opening in append mode
testFile = open('C:\\pyrhon\\Practice Questions\\test1.txt', 'a')
# Loop to copy the lines of one file to other file which does not start with '#'
for i in file:
    String = str(i)
    if(String.startswith('#')):
        continue
    else:
        testFile.write(String)
# Closing of files
file.close()
testFile.close()
