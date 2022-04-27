
import datetime
import os.path
import tempfile

from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site

from typing import Tuple, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


import secrets
import string
from project_management.models import Meeting

from research_portal import settings

import vobject

from email.mime.text import MIMEText

from user.models import Project


class GoogleMananger():
    def __init__(self, access_token) -> None:
        self.__access_token = access_token
        self.__scopes = ['https://www.googleapis.com/auth/calendar']
        self.__creds = Credentials(
            self.__access_token, default_scopes=self.__scopes)

    def create_meeting_link(self, faculty_name, description, start_date, end_date, project_name) -> Tuple[str, str]:
        time_zone = start_date[-6:]
        start_date = start_date[:-6] + ":00"+time_zone

        N = 7

        random_string = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                for i in range(N))

        event = {
            'summary': f'{project_name} Meeting - {faculty_name}',
            'description': description,
            'start': {
                'dateTime': start_date,
            },
            'end': {
                'dateTime': end_date,
            },
            "colorId": 5,
            "conferenceData": {
                "createRequest": {
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    },
                    "requestId": random_string
                }
            },
        }
        service = build('calendar', 'v3', credentials=self.__creds)

        try:
            event = service.events().insert(calendarId='primary', body=event,
                                            conferenceDataVersion=1).execute()

        except HttpError as error:
            print('An error occurred: %s' % error)

        return event['hangoutLink'], event['id']

    def delete_event(self, event_id):
        service = build('calendar', 'v3', credentials=self.__creds)

        event = service.events().delete(calendarId='primary', eventId=event_id).execute()

    def send_meeting_email(self, recipients: List[str], meeting: Meeting, request):
        context = {
            'meeting_link': meeting.link,
            'project_title': meeting.project.title,
            'date_time': meeting.date_time.strftime('%d-%m-%Y %H:%M'),
            'domain': get_current_site(request)
        }
        html_message = render_to_string(
            'student/emails/meeting_invitation.html', context=context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = recipients

        mail = EmailMultiAlternatives(
            f'Invite for Meeting', plain_message, from_email, to)

        mail.attach_alternative(html_message, 'text/html')

        mail.send()
