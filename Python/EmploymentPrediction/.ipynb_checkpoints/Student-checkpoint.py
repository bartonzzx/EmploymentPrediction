class Student():
    def __init__(self,id,natureofunit,workplace):
    # def __init__(self, id, natureofunit, workplace, major):
        self.id = id
        # self.major = major
        self.natureofunit = natureofunit
        self.workplace = workplace
        self.scores = {}
        self.courses = {}

    def descript(self):
        print('学号:' + self.id)
        print('工作性质' + self.natureofunit)
        print('单位名称' + self.workplace)

