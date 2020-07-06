class WithDemo:
    num = 25

    def __enter__(self):
        print('__enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__')
        print(self.num)

    def method1(self,str):
        return  print(str)



with WithDemo() as demo:
    demo.method1(1)
