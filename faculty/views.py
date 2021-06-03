from django.shortcuts import render
from user.decorators import faculty_required


@faculty_required
def home(request, *args, **kwargs):
    return render(request, 'index.html')
