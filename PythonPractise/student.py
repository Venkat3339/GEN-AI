# Write a program to collect all the students information and find who is score maximum

from collections import namedtuple

choice=1
Student = namedtuple('Student', ['id', 'name', 'department', 'score'])
Students = []
while(choice!=-1):
    id = int(input("Enter student ID: "))
    name = input("Enter student name: ")
    department = input("Enter student department: ")
    score = int(input("Enter student score"))
    choice  = int(input("Enter '0' to add new student or '-1' to exit: "))
    Students.append(Student(id, name, department, score))
topScoredStudent = max(Students, key = lambda x : x.score)
print(topScoredStudent)

