class Employee:
    def __init__(self, name, age, city, mobileNumber):
        self.name = name
        self.age = age
        self.city = city
        self.mobileNumber = mobileNumber
    def get(self):
        print("Employee Name: ", self.name)
        print("Employee age: ", self.age)
        print("Employee city: ", self.city)
        print("Employee mobileNumber: ", self.mobileNumber)
class HR (Employee):
    def __init__(self, name, age, city, mobileNumber, projectName):
        super().__init__(name, age, city, mobileNumber)
        self.projectName = projectName
    def get(self):
        super().get()
        print("Employee Project: ", self.projectName)
class HRManager (Employee):
    def __init__(self, name, age, city, mobileNumber, salaryUpdate):
        super().__init__(name, age, city, mobileNumber)
        self.salarryUpdate = salaryUpdate
    def get(self):
        super().get()
        print("Employee Salary: ", self.salarryUpdate)
name = input("Enter Name: ")
age = int(input("Enter Age: "))
city = input("Enter city: ")
mobileNumber = int(input("Enter mobile number: "))

projectName = input("Enter project name: ")
salary = float(input("Enter salary: "))

hr = HR(name, age, city, mobileNumber, projectName)
hrm = HRManager(name, age, city, mobileNumber, salary)
x=20
if(type(hr) == HRManager):
    print("type check")
if(isinstance(x, Employee)):
    print("instance check")


# hr.get()
# hrm.get()