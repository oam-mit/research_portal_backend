from django.urls import path, include
from . import views

app_name = 'project_management_api'

urlpatterns = [
    path('get_meetings/<uuid:project_uuid>/',
         views.get_meetings, name='get_meetings'),

    path('create_meeting/', views.create_meeting, name='create_meeting'),

    # Website urls

]
