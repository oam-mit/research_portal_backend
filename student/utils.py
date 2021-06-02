from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template, render_to_string
from research_portal import settings
from user.models import User, Project
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.views import PasswordResetView

_NEW_APPLICATIONS_NUMBER = 2


def send_application_successful_email(request, user: User, project: Project):

    context = {
        'user': user,
        'project': project,
        'domain': get_current_site(request)
    }

    html_message = render_to_string(
        'student/emails/project_application.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email

    send_mail('Application Submitted Successfully', plain_message,
              from_email, [to], html_message=html_message)


def _send_email_to_professor(request, project: Project):
    context = {
        'faculty': project.faculty,
        'number': _NEW_APPLICATIONS_NUMBER,
        'domain': get_current_site(request)
    }

    html_message = render_to_string(
        'student/emails/project_application.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = project.faculty.user.email

    send_mail('Application Submitted Successfully', plain_message,
              from_email, [to], html_message=html_message)


def check_and_send_professor_email(request, project: Project):
    if project.application_set.count() % _NEW_APPLICATIONS_NUMBER == 0:
        _send_email_to_professor(request, project)
