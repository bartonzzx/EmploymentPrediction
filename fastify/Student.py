class Student():
    def __init__(self,id):
        self.id = id
        self.scores = {}
        self.courses = {}

    def descript(self):
        print('学号:' + self.id)

