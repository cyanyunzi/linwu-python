class Linwu:
    name = ""
    age = 0

    def __init__(self,name,age):
        print("__init__", ":", "实例化自动调用")
        self.name = name
        self.age = age

    def printField(self):
        print("self.name",":",self.name)
        print("self.age",":",self.age)

# 实例化类
linwu = Linwu("林雾",20)
linwu.printField()

