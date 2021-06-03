from django.shortcuts import render
from user.decorators import student_required


@student_required
def home(request, *args, **kwargs):
    return render(request, 'index.html')
