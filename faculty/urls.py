from django.urls import path,include
from . import views

app_name='faculty'

urlpatterns = [
    path('api/',include('faculty.faculty_api.urls')),
    path('home',views.home,name="home"),
    
]

