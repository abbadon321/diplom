from enum import Enum


class Classroom:

    def __init__(self, aud_number):
        self.aud_number = aud_number


class DayOfWeek(Enum):

    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6


class EducationLevel(Enum):

    bachelor = 1
    master = 2
    specialist = 3
    doctor = 4


class Group:

    def __init__(self, group_name, educ_lvl, course):
        self.group_name = group_name
        self.educ_lvl = educ_lvl
        self.course = course


class Lecturer:

    def __init__(self, name):
        self.name = name


class Parity(Enum):

    everyWeek = 1
    onEvenWeek = 2
    onOddWeek = 3


class Subject:

    def __init__(self, subject_name):
        self.subject_name = subject_name


class Time:

    def __init__(self, start, end):
        self.start = start
        self.end = end


class TypeOfLearningActivity(Enum):

    labs = 1
    lecture = 2
    practice = 3


class User:

    def __init__(self, login, password):
        self.login = login
        self.password = password


# ???
class Class(Subject, Group, Lecturer, DayOfWeek, Time, Classroom, Parity,
            TypeOfLearningActivity):

    def __init__(self, subject, group, lecturer, day, time, classroom,
                 is_sub_divided, parity, activity, is_online):
        self.subject = subject
        self.group = group
        self.lecturer = lecturer
        self.day = day
        self.time = time
        self.classroom = classroom
        self.is_sub_divided = is_sub_divided
        self.parity = parity
        self.activity = activity
        self.is_online = is_online
