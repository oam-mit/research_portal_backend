from django.db import models

from user.models import Project, Student

# Create your models here.


class Task(models.Model):
    student = models.ForeignKey(
        to=Student, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    description = models.TextField(max_length=64000)

    def __str__(self) -> str:
        return self.description


class Meeting(models.Model):
    students = models.ManyToManyField(to=Student)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    link = models.URLField()
    date_time = models.DateTimeField()
    description = models.TextField(max_length=40000)

    def __str__(self) -> str:
        return f'{self.link}-> {self.date_time}'
