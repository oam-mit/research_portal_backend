from django.contrib.auth.forms import AuthenticationForm,UsernameField,UserCreationForm
from django import forms

from .models import User,Department,Student,Faculty

class CustomAuthenticationForm(AuthenticationForm):
    username=UsernameField(
        widget=forms.TextInput(attrs={'autofocus': False,'class':'form-control bg-white border-left-0 border-md','placeholder':'Email'})
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control bg-white border-left-0 border-md','placeholder':'Password'}),
    )


class CustomUserCreationForm(UserCreationForm):

    email=forms.EmailField(
        label=("Email (Will be used to login and send emails)"),
        widget=forms.EmailInput(attrs={'class':'form-control bg-white border-left-0 border-md','autofocus':False,'placeholder':'Enter your Learner Id'}),
    )
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control bg-white border-left-0 border-md','placeholder':'Enter your password'}),
        help_text=('Enter a strong password<br>Do not keep password too similar to email<br>Password should be more than 8 characters<br><br>'),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control bg-white border-left-0 border-md','placeholder':'Password Confirmation'}),
        strip=False,
        help_text=("Enter the same password as before, for verification<br>"),
    )

    first_name=forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'First Name'}),
        label=("Enter First Name")
    )

    last_name=forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control bg-white border-left-0 border-md','placeholder':'Last Name'}),
        label=("Enter Last Name")
    )

    department=forms.ModelChoiceField(
        queryset=Department.objects.all(),empty_label='Select your department',widget=forms.Select(attrs={'class':'custom-select bg-white border-md border-left-0 pl-3'})
    )
    class Meta:
        model=User
        fields=['email','first_name','last_name','department','password1','password2']

    def save(self,is_faculty=True,*args,**kwargs):
        user=super().save(commit=False,*args,**kwargs)
        user.is_active=False
        if is_faculty:
            user.is_faculty=True
        else:
            user.is_student=True
        user.save()
        return user


class StudentCreationForm(forms.ModelForm):
    registration_number=forms.CharField(
        widget=forms.NumberInput(attrs={'placeholder':'Registration Number','class':'form-control bg-white border-left-0 border-md'})
    )


    class Meta:
        model=Student
        fields=['registration_number']


