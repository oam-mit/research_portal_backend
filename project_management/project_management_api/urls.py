from django.urls import path, include
from . import views

app_name = 'project_management_api'

urlpatterns = [
    path('get_meetings/<uuid:project_uuid>/',
         views.get_meetings, name='get_meetings'),

    path('create_meeting/', views.create_meeting, name='create_meeting'),

    path('get_tasks/<uuid:project_uuid>/', views.get_tasks, name="get_tasks"),

    path('change_task_status/', views.change_task_status,
         name="change_task_status"),

    path('create_task/', views.create_task, name="create_task"),

    # Website urls

]
