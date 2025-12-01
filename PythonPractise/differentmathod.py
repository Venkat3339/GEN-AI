class Demo:
    x = 10
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def instanceMothod(self):    # instance mothod
        print(self.x)
        print("It is an instance mathod")
    @classmethod
    def classMathod(cls):   
        print(cls.x)    # class mathod
        print("It is a class mathod")
    @staticmethod
    def staticMathod(y): 
        # print(self.x)     # static mathod
        print("It is a static mathod",y)

Demo.classMathod()
Demo.staticMathod(29)
obj = Demo("Sarath", 23)
obj.instanceMothod()
obj.classMathod()
obj.staticMathod(20)