# Write a Python script that reads a text file line by line and prints only the lines containing the word “Python” (case-insensitive).

# File reading
file = open('C:\\pyrhon\\Practice Questions\\test.txt', 'r')
# reading the content of the file till end of the line
lines = file.readlines()
# Loop that prints the line contining the word python
for i in lines:
    str = i.lower()
    if('python' in str):
        print(i)
# File closing
file.close()
    
    
  
