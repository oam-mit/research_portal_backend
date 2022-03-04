import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import secrets
import string


class GoogleMananger():
    def __init__(self, access_token) -> None:
        self.__access_token = access_token
        self.__scopes = ['https://www.googleapis.com/auth/calendar']
        self.__creds = Credentials(
            self.__access_token, default_scopes=self.__scopes)

    def create_meeting_link(self, faculty_name, description, start_date, end_date, project_name) -> str:
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

        return event['hangoutLink']
