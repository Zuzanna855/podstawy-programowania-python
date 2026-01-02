class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks


    def is_passed(self):
        if sum(self.marks) / len(self.marks) > 50:
            return True
        else:
            return False


student1 = Student(name="Marek", marks=[50, 20, 30, 10])
student2 = Student(name="", marks=[50, 60, 70, 80])
print(student1.is_passed())
print(student2.is_passed())



