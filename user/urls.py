from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path,include

from .forms import CustomAuthenticationForm
from . import views
app_name='user'

urlpatterns = [
    path(
        '',views.login,name='login'),
    path('logout',views.logout),

    path('redirect_accordingly',views.signin_redirect,name="redirect_accordingly"),
    path('api/get_logged_in_user/',views.get_logged_in_user,name="get_logged_in_user"),

    path('student/register',views.register_student,name='student_register'),
    path('faculty/register',views.register_faculty,name="faculty_register"),


]

