# Create a program that accepts a number and prints all factors of that number using a for loop.

# input Reading
value = int(input("Enter the number: "))
factorsCollection = [1]
# Loop that collect all the factor of a given number into a list6
for i in range(2,value):
    if(value % i == 0):
        factorsCollection.append(i)
factorsCollection.append(value)
# Printing the all collected factors of a number
print("Total factors of the give number: ", factorsCollection)