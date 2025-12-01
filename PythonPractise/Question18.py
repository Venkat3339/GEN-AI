# Using nested if-else, write a program that classifies a triangle as equilateral, isosceles, or scalene based on user input sides.

# input reading 
side1 = int(input("Enter a value: "))
side2 = int(input("Enter a value: "))
side3 = int(input("Enter a value: "))
# If-elif-else block to check the type of triangle
if(side1 == side2 and side2 == side3):
    print("Triangle is equilateral triangle")
elif((side1 == side2 and side2 != side3) or (side1 == side3 and side3 != side2) or (side2 == side3 and side3 != side1)):
    print("Triangle is isosceles triangle")
else:
    print("Triangle is scalene triangle")