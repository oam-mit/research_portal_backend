from django.contrib.auth.forms import AuthenticationForm,UsernameField,UserCreationForm
from django import forms

from .models import User,Department,Student,Faculty

class CustomAuthenticationForm(AuthenticationForm):
    username=UsernameField(
        widget=forms.TextInput(attrs={'autofocus': False,'class':'form-control','placeholder':'Email'})
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control','placeholder':'Password'}),
    )


class CustomUserCreationForm(UserCreationForm):

    email=forms.EmailField(
        label=("Email (Will be used to login and send emails)"),
        widget=forms.EmailInput(attrs={'class':'form-control','autofocus':False,'placeholder':'Enter your Learner Id'}),
    )
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control','placeholder':'Enter your password'}),
        help_text=('Enter a strong password<br>Do not keep password too similar to email<br>Password should be more than 8 characters<br><br>'),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control','placeholder':'Re-enter your password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification<br>"),
    )

    first_name=forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
        label=("Enter First Name")
    )

    last_name=forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
        label=("Enter Last Name")
    )

    department=forms.ModelChoiceField(
        queryset=Department.objects.all(),empty_label='Select your department',widget=forms.Select(attrs={'class':'form-control'})
    )
    class Meta:
        model=User
        fields=['email','first_name','last_name','department','password1','password2']

    def save(self,is_faculty,*args,**kwargs):
        user=super().save(commit=False,*args,**kwargs)
        if is_faculty:
            user.is_faculty=True
        else:
            user.is_student=True
        user.save()
        return user


class StudentCreationForm(forms.ModelForm):
    registration_number=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Registration Number','class':'form-control'})
    )


    class Meta:
        model=Student
        fields=['registration_number']


