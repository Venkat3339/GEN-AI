# Write a Python script that reads a list of marks and prints “Pass” if all marks are above 40, otherwise “Fail”, using logical AND.

# input reading 
teluguMarks = int(input("Enter the marks: "))
hindiMarks = int(input("Enter the marks: "))
engilishMarks = int(input("Enter the marks: "))
mathsMarks = int(input("Enter the marks: "))
# If-else block to know the student is pass or fail
if(teluguMarks > 40 and hindiMarks > 40 and engilishMarks > 40 and mathsMarks > 40):
    print("Pass")
else:
    print("Fail")
