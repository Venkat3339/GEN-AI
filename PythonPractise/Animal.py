class Mammal:
    def birth(self):
        print("Mammal can give birth to living beings")
class Birds:
    def fly(self):
        print("Birds can fly and lay egg to give birth")
class Bat (Mammal, Birds):
    def func(self):
        print("Bat is an flying mammal")
obj = Bat()
obj.func()
obj.fly()
obj.birth() 
print(Bat.__mro__)
