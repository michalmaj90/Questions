from django.db import models


SCHOOL_CLASS = (
    (1, "1a"),
    (2, "1b"),
    (3, "2a"),
    (4, "2b"),
    (5, "3a"),
    (6, "3b"),
)

GRADES = (
    (1, "1"),
    (1.5, "1+"),
    (1.75, "2-"),
    (2, "2"),
    (2.5, "2+"),
    (2.75, "3-"),
    (3, "3"),
    (3.5, "3+"),
    (3.75, "4-"),
    (4, "4"),
    (4.5, "4+"),
    (4.75, "5-"),
    (5, "5"),
    (5.5, "5+"),
    (5.75, "6-"),
    (6, "6")
)

# Create your models here.
class SchoolSubject(models.Model):
    name = models.CharField(max_length=64)
    teacher_name = models.CharField(max_length=64)

    @property
    def t_name(self):
        return "{}".format(self.teacher_name)

    def __str__(self):
        return self.t_name


class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name =  models.CharField(max_length=64)
    school_class = models.IntegerField(choices=SCHOOL_CLASS)
    year_of_birth = models.IntegerField(null=True)
    grades = models.ManyToManyField(SchoolSubject, through="StudentGrades")

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name


class StudentGrades(models.Model):
    student = models.ForeignKey(Student)
    school_subject = models.ForeignKey(SchoolSubject)
    grade = models.FloatField(choices=GRADES)

    @property
    def __float__(self):
        return self.grade

class PresenceList(models.Model):
    student = models.ForeignKey(Student)
    day = models.DateField()
    present = models.NullBooleanField(null=True)


class Message(models.Model):
    subject = models.CharField(max_length=256)
    content = models.TextField()
    to = models.ForeignKey(SchoolSubject)
    from_who = models.ForeignKey(Student)
    date_sent = models.DateTimeField(auto_now_add=True, blank=True)


class StudentNotice(models.Model):
    from_who = models.ForeignKey(SchoolSubject)
    to = models.ForeignKey(Student)
    content = models.TextField()

    @property
    def notices(self):
        return "{}".format(self.content)

    def __str__(self):
        return self.notices
