
from django.urls import path, include
from . import views

app_name = 'student_api'

urlpatterns = [
    path('get_departments/', views.get_departments, name='api_get_departments'),
    path('get_projects/<str:department_slug>/',
         views.get_projects, name="api_get_projects"),
    path('submit_application/', views.submit_application,
         name="api_submit_application"),
    path('get_applied_projects/', views.get_applied_projects,
         name="api_get_applied_projects"),
    path('submit_cv/', views.submit_cv, name="api_submit_cv"),
    path('change_domains_of_interest/', views.edit_domain_of_interest,
         name="change_domains_of_interest"),
    path('get_working_on_projects/', views.get_working_on_projects,
         name="get_working_on_projects"),
]
