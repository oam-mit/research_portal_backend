
from django.urls import path,include
from . import views

app_name='student'

urlpatterns = [
    path('api/get_departments/',views.get_departments,name='api_get_departments'),
    path('api/get_projects/<str:department_slug>/',views.get_projects,name="api_get_projects"),
    path('api/submit_application/',views.submit_application,name="api_submit_application"),
    path('api/get_applied_projects/',views.get_applied_projects,name="api_get_applied_projects"),
    path('api/submit_cv/',views.submit_cv,name="api_submit_cv"),
]

