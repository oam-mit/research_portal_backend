import re
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
    if not email.endswith('@learner.manipal.edu'):
        raise ValidationError(
        ('Please enter your Learner Id (@learner.manipal.edu)')
)


def check_registration_number(registration_number:str):
    regex=re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if registration_number.isalpha() or regex.search(registration_number) == None:
        raise ValidationError(
            ('Enter a valid registration number')
    )


class User(AbstractUser):

    email=models.EmailField(validators=[email_validator],unique=True)
    username=None

    department=models.ForeignKey(to='Department',on_delete=models.SET_NULL,null=True)

    is_faculty=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']

    objects=CustomUserManager()


    def __str__(self):
        return self.email

    class Meta:
        unique_together=['first_name','last_name']
        
    

class Student(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE)
    registration_number=models.CharField(max_length=10,validators=[])
    cv=models.FileField(upload_to='student/CVs',null=True,blank=True)

    def __str__(self):
        return self.user.email


class Faculty(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='faculty/pics',blank=True,null=True)

    def __str__(self):
        return self.user.email


class Department(models.Model):
    name=models.CharField(max_length=6000,unique=True)
    department_building=models.CharField(max_length=600)
    slug=models.SlugField(max_length=100,blank=True)


    def __str__(self):
        return self.name


@receiver(pre_save,sender=Department)
def slugify_department(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


class Project(models.Model):
    id=models.BigAutoField(primary_key=True)
    uuid_field=models.UUIDField(unique=True,default=uuid4,editable=False)
    faculty=models.ForeignKey(to=Faculty,on_delete=models.CASCADE)
    title=models.CharField(max_length=6000)
    description=models.TextField(max_length=65000)
    tags=models.CharField(max_length=65000)
    is_department_specific=models.BooleanField()
    max_students=models.PositiveBigIntegerField()
    start_date=models.DateField()
    end_date=models.DateField()
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    project=models.ForeignKey(to=Project,on_delete=models.CASCADE)
    student=models.ForeignKey(to=Student,on_delete=models.CASCADE)
    time_of_submission=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.user.email+" "+self.project.title
    
    class Meta:
        unique_together=['project','student']