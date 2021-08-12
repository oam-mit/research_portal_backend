from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from research_portal import settings
from user.models import ACCEPTED, REJECTED, Application, Project, User


class FacultyEmail():

    def send_application_status_change_email(self, request, application: Application):

        if application.status == ACCEPTED:
            self. __send_acceptance_email(request, application)
        elif application.status == REJECTED:
            self.__send_rejection_email(request, application)

    def __send_acceptance_email(self, request, application: Application):
        context = {
            'student': application.student,
            'project': application.project,
            'faculty': application.project.faculty,
            'domain': get_current_site(request)
        }

        html_message = render_to_string(
            'faculty/emails/application_acceptance_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = application.student.user.email

        send_mail('Acceptance of Application', plain_message,
                  from_email, [to], html_message=html_message)

    def __send_rejection_email(self, request, application: Application):

        context = {
            'student': application.student,
            'project': application.project,
            'faculty': application.project.faculty,
            'domain': get_current_site(request)
        }

        html_message = render_to_string(
            'faculty/emails/application_rejection_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = application.student.user.email

        send_mail('Application Update', plain_message,
                  from_email, [to], html_message=html_message)


# def send_application_status_change_email(request, application: Application):

#     if application.status == ACCEPTED:
#         __send_acceptance_email(request, application)
#     elif application.status == REJECTED:
#         __send_rejection_email(request, application)


# def __send_acceptance_email(request, application: Application):
#     context = {
#         'student': application.student,
#         'project': application.project,
#         'faculty': application.project.faculty,
#         'domain': get_current_site(request)
#     }

#     html_message = render_to_string(
#         'faculty/emails/application_acceptance_email.html', context)
#     plain_message = strip_tags(html_message)
#     from_email = settings.EMAIL_HOST_USER
#     to = application.student.user.email

#     send_mail('Acceptance of Application', plain_message,
#               from_email, [to], html_message=html_message)


# def __send_rejection_email(request, application: Application):

#     context = {
#         'student': application.student,
#         'project': application.project,
#         'faculty': application.project.faculty,
#         'domain': get_current_site(request)
#     }

#     html_message = render_to_string(
#         'faculty/emails/application_rejection_email.html', context)
#     plain_message = strip_tags(html_message)
#     from_email = settings.EMAIL_HOST_USER
#     to = application.student.user.email

#     send_mail('Application Update', plain_message,
#               from_email, [to], html_message=html_message)
