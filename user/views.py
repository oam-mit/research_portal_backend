#Django Packages
from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#Rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

#My Packages
from .models import Student,Faculty
from .forms import CustomUserCreationForm,StudentCreationForm
from .serializers import UserSerializer
# Create your views here.

def register_student(request):
    context={}

    if request.method=='POST':
        user_form=CustomUserCreationForm(request.POST)
        student_form=StudentCreationForm(request.POST)
        if user_form.is_valid():
            user=user_form.save(is_faculty=False)
            student=Student.objects.create(user=user,registration_number=request.POST.get('registration_number'))
            messages.success(request,'Account Created successfully')
            return redirect(reverse('user:login'))
        else:
            context['user_form']=user_form
            context['student_form']=student_form
            messages.error(request,'Please check your inputs',extra_tags='danger')
            return render(request,'user/student_register.html',context=context)


    user_form=CustomUserCreationForm()
    student_form=StudentCreationForm()
    context['user_form']=user_form
    context['student_form']=student_form
    return render(request,'user/student_register.html',context=context)


def register_faculty(request):
    context={}

    if request.method=='POST':
        user_form=CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user=user_form.save(is_faculty=True)
            faculty=Faculty.objects.create(user=user)
            return redirect(reverse('user:login'))
        else:
            context['user_form']=user_form
            messages.error(request,'Please check your inputs',extra_tags='danger')
            return render(request,'user/faculty_register.html',context=context)




    user_form=CustomUserCreationForm()
   
    context['user_form']=user_form

    return render(request,'user/faculty_register.html',context=context)
        



@login_required
def signin_redirect(request):
    if request.user.is_student:
        return redirect(reverse('student:api_get_departments'))
    else:
        return redirect(reverse('faculty:faculty_home'))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user(request):
    context={}

    serializer=UserSerializer(request.user)
    context['user']=serializer.data

    return Response(context)