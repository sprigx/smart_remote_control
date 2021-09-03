import time

class Test:
    def __init__(self):
        time.sleep(5) # 重い処理
        self.a = 1
        self.b = 2

    def execute(self, operation):
        if operation == '+':
            return self.a + self.b
        elif operation == '-':
            return self.a - self.b
        else:
            return 'unknown operation'


