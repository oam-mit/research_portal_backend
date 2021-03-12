from django.urls import path,include
from . import views

app_name='faculty'

urlpatterns = [
    path('api/get_active_projects/',views.get_active_projects,name='api_get_active_projects'),
    path('api/get_applicants/<str:project_uuid>/',views.get_applicants,name="api_get_applicants"),
    path('api/submit_project/',views.submit_project,name="api_submit_project"),
    path('api/update_profile_picture/',views.update_profile_picture,name="api_update_profile_picture"),
]

