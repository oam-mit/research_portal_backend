import re
import os

from uuid import uuid4

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .managers import CustomUserManager


# Create your models here.


def email_validator(email):
    if not email.endswith('manipal.edu'):
        raise ValidationError(
            ('Please enter your valid Manipal Email Id (ends with manipal.edu)')
        )


def check_registration_number(registration_number: str):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if registration_number.isalpha() or regex.search(registration_number) == None:
        raise ValidationError(
            ('Enter a valid registration number')
        )


class User(AbstractUser):

    email = models.EmailField(validators=[email_validator], unique=True)
    username = None

    department = models.ForeignKey(
        to='Department', on_delete=models.SET_NULL, null=True)

    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        unique_together = ['first_name', 'last_name']


def upload_and_rename_cv(instance, filename):
    upload_to = 'student/CVs'
    extension = filename.split('.')[-1]

    (first_name, last_name, registration_number) = (instance.user.first_name,
                                                    instance.user.last_name, instance.registration_number)

    return os.path.join(upload_to, f'{registration_number}_{first_name}_{last_name}.{extension}')


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=10, validators=[])
    cv = models.FileField(upload_to=upload_and_rename_cv,
                          null=True, blank=True)

    domains_of_interest = models.CharField(max_length=65000, null=True)

    def __str__(self):
        return self.user.email


def upload_and_rename_pic(instance, filename):
    upload_to = 'faculty/pics'
    extension = filename.split('.')[-1]

    (first_name, last_name) = (instance.user.first_name, instance.user.last_name)

    return os.path.join(upload_to, f'{first_name}_{last_name}.{extension}')


DESIGNATION_CHOICES = [
    ('Mr', 'Mr'),
    ('Ms', 'Ms'),
    ('Mrs', 'Mrs'),
    ('Dr', 'Dr'),
]


class Faculty(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    # add designation
    designation = models.CharField(
        default='Mr', choices=DESIGNATION_CHOICES, max_length=10)
    profile_picture = models.ImageField(
        upload_to=upload_and_rename_pic, blank=True, null=True)

    def __str__(self):
        return self.user.email


class Department(models.Model):
    name = models.CharField(max_length=6000, unique=True)
    department_building = models.CharField(max_length=600)
    slug = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Department)
def slugify_department(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid_field = models.UUIDField(unique=True, default=uuid4, editable=False)
    faculty = models.ForeignKey(to=Faculty, on_delete=models.CASCADE)
    # page 1
    title = models.CharField(max_length=6000)
    description = models.TextField(max_length=65000)
    outcome = models.CharField(null=True, max_length=2000)
    tags = models.CharField(max_length=65000)

    # page2
    is_department_specific = models.BooleanField()
    is_extendable = models.BooleanField(default=False)
    max_students = models.PositiveBigIntegerField()
    hours_per_week = models.PositiveIntegerField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


APPPLIED = 'applied'
REJECTED = 'rejected'
ACCEPTED = 'accepted'

STATUS_CHOICES = [
    (APPPLIED, APPPLIED[0].upper()+APPPLIED[1:]),
    (REJECTED, REJECTED[0].upper()+REJECTED[1:]),
    (ACCEPTED, ACCEPTED[0].upper()+ACCEPTED[1:]),
]


class Application(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    time_of_submission = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=100, default='applied')

    def __str__(self):
        return self.student.user.email+" "+self.project.title

    class Meta:
        unique_together = ['project', 'student']


class Feedback(models.Model):
    application = models.OneToOneField(
        to=Application, on_delete=models.CASCADE)
    project_is_complete = models.BooleanField()
    feedback = models.CharField(max_length=20000)

    def __str__(self) -> str:
        return self.feedback
