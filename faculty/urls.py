from django.urls import path, include
from . import views

app_name = 'faculty'

urlpatterns = [
    path('api/', include('faculty.faculty_api.urls')),

    # Website urls
    path('home', views.home, name="home"),
    path('applications/<uuid:project_uuid>',
         views.home, name="project_applications"),
    path('applications/accepted/<uuid:project_uuid>',
         views.home, name="accepted_applications"),
    path('profile', views.home, name="profile"),
    path('project/add', views.home, name="add_project"),
]
