
from django.urls import path,include
from . import views

app_name='student'

urlpatterns = [
    path('api/',include('student.student_api.urls')),
    path('home',views.home,name="home")
]

