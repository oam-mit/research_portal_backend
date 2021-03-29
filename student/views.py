from django.shortcuts import render
from user.decorators import student_required


@student_required
def home(request):
    return render(request,'index.html')