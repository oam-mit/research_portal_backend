from django.urls import path, include
from . import views

app_name = 'project_management'

urlpatterns = [
    path('api/', include('project_management.project_management_api.urls')),

    # Website urls

]
