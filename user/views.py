# Django Packages
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout as logout_user, login as login_user, authenticate
from django.db import transaction

# Rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# My Packages
from .models import Student, Faculty
from .forms import CustomUserCreationForm, ResendVerificationForm, StudentCreationForm, CustomAuthenticationForm, FacultyRegistrationForm
from .serializers import UserSerializer
from research_portal.settings import LOGIN_REDIRECT_URL

# Verification email
from .email_handler import send_verification_email, resend_verification_email as resend

# Create your views here.


def login(request):
    context = {}
    next = request.GET.get('next')
    if request.user.is_authenticated:
        if not next:  # If there is a next parameter means that there is a redirected response
            return redirect(reverse(LOGIN_REDIRECT_URL))
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        user = authenticate(request, username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user is not None:
            login_user(request, user)
            if next:
                return redirect(next)
            return redirect(reverse(LOGIN_REDIRECT_URL))
        else:
            context['form'] = form
            messages.error(
                request, 'Please enter valid Email Id and password. Kindly note that both email id and password are case-sensitive')
            return render(request, 'user/login.html', context=context)

    form = CustomAuthenticationForm()
    context['form'] = form
    return render(request, 'user/login.html', context=context)


@transaction.atomic
def register_student(request):
    context = {}

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentCreationForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():

            if user_form.cleaned_data.get('email').endswith('@manipal.edu'):
                messages.error(
                    request, 'Please enter your learner id (ends with @learner.manipal.edu)')
                context['user_form'] = user_form
                context['student_form'] = student_form
                return render(request, 'user/student_register.html', context=context)

            user = send_verification_email(request, False, user_form)
            try:
                student = Student.objects.create(
                    user=user, registration_number=request.POST.get('registration_number'))

                messages.success(
                    request, 'Account Created successfully. Please check your inbox for the confirmation email. Failure to confirm your email id would result in failure to log in to your account')
                return redirect(reverse('user:login'))
            except:
                transaction.set_rollback(True)
                context['user_form'] = user_form
                context['student_form'] = student_form
                messages.error(
                    request, 'Internal Error occurred. Please try after sometime', extra_tags='danger')
                return redirect(reverse('user:student_register'))
        else:
            context['user_form'] = user_form
            context['student_form'] = student_form
            return render(request, 'user/student_register.html', context=context)

    user_form = CustomUserCreationForm()
    student_form = StudentCreationForm()
    context['user_form'] = user_form
    context['student_form'] = student_form
    return render(request, 'user/student_register.html', context=context)


def register_faculty(request):
    context = {}

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        faculty_form = FacultyRegistrationForm(request.POST)
        if user_form.is_valid() and faculty_form.is_valid():
            if user_form.cleaned_data.get('email').endswith('@learner.manipal.edu'):
                messages.error(
                    request, 'Please enter your manipal id (ends with @manipal.edu)')
                context['user_form'] = user_form
                context['student_form'] = faculty_form
                return render(request, 'user/faculty_register.html', context=context)

            user = send_verification_email(request, True, user_form)
            faculty = Faculty.objects.create(
                user=user, designation=faculty_form.cleaned_data.get('designation'))
            messages.success(
                request, 'Account Created successfully. Please check your inbox for the confirmation email. Failure to confirm your email id would result in failure to log in to your account')
            return redirect(reverse('user:login'))
        else:
            context['user_form'] = user_form
            context['faculty_form'] = faculty_form
            messages.error(request, 'Please check your inputs',
                           extra_tags='danger')
            return render(request, 'user/faculty_register.html', context=context)

    user_form = CustomUserCreationForm()
    faculty_form = FacultyRegistrationForm()

    context['user_form'] = user_form
    context['faculty_form'] = faculty_form

    return render(request, 'user/faculty_register.html', context=context)


@login_required
def signin_redirect(request):
    if request.user.is_student:
        return redirect(reverse('student:home'))
    else:
        return redirect(reverse('faculty:home'))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user(request):
    context = {}

    serializer = UserSerializer(request.user)
    context['user'] = serializer.data

    return Response(context)


def logout(request):
    logout_user(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect(reverse('user:login'))


def resend_verification_email(request):
    context = {}
    if request.method == 'POST':
        form = ResendVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)

            try:

                user = get_user_model().objects.get(email=email, is_active=False)
                resend(request, user)

            except Exception as e:
                print(e.__str__())
            return redirect(reverse('user:resend_complete'))

    form = ResendVerificationForm()

    context['form'] = form

    return render(request, 'user/verification_email/resend_verification.html', context=context)


def resend_verification_complete(request):
    return render(request, 'user/verification_email/successfully_sent.html')
