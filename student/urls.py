
from django.urls import path, include
from . import views

app_name = 'student'

urlpatterns = [
    path('api/', include('student.student_api.urls')),

    # Website Urls:
    path('home', views.home, name="home"),
    path('department/<slug:department_slug>', views.home, name="department"),
    path('<slug:department_slug>/project/<uuid:uuid_field>',
         views.home, name="project"),
    path('applications', views.home, name="applications"),
    path('profile', views.home, name="profile"),

]
