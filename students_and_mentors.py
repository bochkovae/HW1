from functools import total_ordering
from itertools import count


@total_ordering
class Student:

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and self.grade_correct(grade)
                and course in lecturer.courses_attached
                and (course in self.courses_in_progress
                     or course in self.finished_courses)):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
            return True
        return False

    def grade_correct(self, grade):
        if isinstance(grade, int) and 0 < grade < 11:
            return True
        return False

    def get_avg_score(self):
        scores = 0
        count_score = 0
        for _, grade in self.grades.items():
            scores += sum(grade)
            count_score += len(grade)
        if count_score:
            return round(scores/count_score, 1)
        return '0'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\n"\
            f"Средняя оценка за домашние задания: {self.get_avg_score()}\n"\
            f"Курсы в процессе изучения: "\
            f"{', '.join(self.courses_in_progress)} \n"\
               f"Завершенные курсы: {', '.join(self.finished_courses)}"

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.get_avg_score() == other.get_avg_score()
        return 'Ошибка'

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.get_avg_score() < other.get_avg_score()
        return 'Ошибка'


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def get_avg_score(self):
        scores = 0
        count_score = 0
        for _, grade in self.grades.items():
            scores += sum(grade)
            count_score += len(grade)
        if count_score:
            return round(scores/count_score, 1)
        return 0

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\n"\
               f"Средняя оценка за лекции: {self.get_avg_score()}"

    def __eq__(self, other):
        if isinstance(other, Lecturer):
            return self.get_avg_score() == other.get_avg_score()
        return 'Ошибка'

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.get_avg_score() < other.get_avg_score()
        return 'Ошибка'


class Reviewer(Mentor):

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and course in self.courses_attached
                and course in student.courses_in_progress
                and self.grade_correct(grade)):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def grade_correct(self, grade):
        if isinstance(grade, int) and 0 < grade < 11:
            return True
        return False

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


def students_avg_rating(students_list, course):
    scores = 0
    count_score = 0
    for student in students_list:
        if isinstance(student, Student):
            if course in student.grades:
                scores += sum(student.grades[course])
                count_score += len(student.grades[course])
    if scores:
        return round(scores/count_score, 1)
    return 0


def lecturers_avg_rating(lecturers_list, course):
    scores = 0
    count_score = 0
    for lecturer in lecturers_list:
        if isinstance(lecturer, Lecturer):
            if course in lecturer.grades:
                scores += sum(lecturer.grades[course])
                count_score += len(lecturer.grades[course])
    if scores:
        return round(scores/count_score, 1)
    return 0

if __name__ == "__main__":
    student1 = Student("Tom", "Pane", "male")
    student2 = Student("Maria", "Osipova", "female")

    student1.courses_in_progress += ["Math", "Physics"]
    student1.finished_courses += ['Python']
    student2.courses_in_progress += ["Singing", "Dancing"]
    student2.finished_courses += ["Math"]

    lecturer1 = Lecturer("Tony", "Stark")
    lecturer1.courses_attached += ["Math", "Physics", "Python"]
    lecturer2 = Lecturer("Melissa", "Spider")
    lecturer2.courses_attached += ['Singing', 'Dancing']

    reviewer1 = Reviewer("Sid", "Mayer")
    reviewer1.courses_attached = ["Math", "Physics", "Python"]
    reviewer2 = Reviewer("Alica", "Kopperfield")
    reviewer2.courses_attached += ["Singing", "Dancing"]

    student1.rate_lecturer(lecturer1, 'Python', 9)
    student1.rate_lecturer(lecturer1, 'Math', 10)
    student1.rate_lecturer(lecturer1, 'Math', 8)
    student1.rate_lecturer(lecturer1, 'Physics', 10)

    student2.rate_lecturer(lecturer2, "Singing", 8)
    student2.rate_lecturer(lecturer2, "Dancing", 10)
    student2.rate_lecturer(lecturer1, "Math", 10)

    reviewer1.rate_hw(student1, 'Math', 10)
    reviewer1.rate_hw(student1, 'Math', 3)
    reviewer1.rate_hw(student1, 'Math', 8)
    reviewer1.rate_hw(student1, 'Math', 10)
    reviewer1.rate_hw(student1, 'Physics', 10)
    reviewer1.rate_hw(student2, 'Math', 9)
    reviewer1.rate_hw(student2, 'Math', 10)

    reviewer2.rate_hw(student2, 'Singing', 10)
    reviewer2.rate_hw(student2, 'Singing', 8)
    reviewer2.rate_hw(student2, 'Singing', 6)
    reviewer2.rate_hw(student2, 'Dancing', 10)
    print(f"Студент 1:\n{student1}")
    print(f"Студент 2:\n{student2}")
    print(f"Лектор 1:\n{lecturer1}")
    print(f"Лектор 2:\n{lecturer2}")
    print(f"Ревьюер 1:\n{reviewer1}")
    print(f"Ревьюер 2:\n{reviewer2}")

    print("Средняя оценка лекторов за курс Math:",
          lecturers_avg_rating([lecturer1, lecturer2], 'Math'))
    print("Средняя оценка студентов за курс Math:",
          students_avg_rating([student1, student2], 'Math'))
    print(f"Лектор 1 круче лектора 2: {lecturer1 > lecturer2}")
    print(f"Студент 1 круче студента 2: {student1 > student2}")



