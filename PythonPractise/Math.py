class Math:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def addition(self):
        sum = self.a+self.b
        print("Addition: ", sum)
    def subtraction(self):
        sub = self.a-self.b
        print("Subtraction: ", sub)
    def multiply(self):
        product = self.a*self.b
        print("Multiplication: ",product)
    def division(self):
        divide = self.a/self.b
        print("Division: ", divide)
num1 = int(input("Enter a number 1: "))
num2 = int(input("Enter a number 2: "))
obj = Math(num1,num2)
obj.addition()
obj.subtraction()
obj.multiply()
obj.division()