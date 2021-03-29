from django.urls import path,include
from . import views

app_name='faculty_api'

urlpatterns = [
    path('get_active_projects/',views.get_active_projects,name='api_get_active_projects'),
    path('get_applicants/<str:project_uuid>/',views.get_applicants,name="api_get_applicants"),
    path('get_accepted_applicants/<str:project_uuid>/',views.get_accepted_applicants,name="api_get_accepted_applicants"),
    path('submit_project/',views.submit_project,name="api_submit_project"),
    path('update_profile_picture/',views.update_profile_picture,name="api_update_profile_picture"),
    path('application_change_status/',views.application_change_status,name="api_application_change_status"),
]

