from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from faculty.serializers import UserApplicationSerializer
from project_management.project_management_api.serializers import MeetingSerializer
from project_management.project_management_api.utils import GoogleMananger
from user.models import ACCEPTED, Application, Project


from user.permissions import IsFaculty


from project_management.models import Meeting
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meetings(request, project_uuid):
    context = {}

    accepted_applicants = Application.objects.filter(
        project__faculty=request.user.faculty, project__uuid_field=project_uuid, status=ACCEPTED)

    application_serializer = UserApplicationSerializer(
        accepted_applicants, many=True)
    context['accepted_applications'] = application_serializer.data

    meetings = Meeting.objects.filter(
        project__uuid_field=project_uuid).order_by('-date_time')

    serializer = MeetingSerializer(meetings, many=True)

    context['meetings'] = serializer.data
    return Response(context)


@api_view(['POST'])
def create_meeting(request):
    context = {}
    google_manager = GoogleMananger(
        access_token=request.data.get('access_token'))

    try:
        project = Project.objects.get(
            uuid_field=request.data.get('uuid_field'))

        link = google_manager.create_meeting_link(
            f'{project.faculty.designation}.{project.faculty.user.first_name} {project.faculty.user.last_name}',
            request.data.get('description'),
            request.data.get('start_date'),
            request.data.get('end_date'),
            project.title
        )

        meeting = Meeting.objects.create(
            link=link,
            project=project,
            date_time=request.data.get('start_date'),
            description=request.data.get('description')
        )
        serializer = MeetingSerializer(meeting)
        context['status'] = 'successful'
        context['meeting'] = serializer.data

        return Response(context)
    except Exception as e:
        context['status'] = 'unsuccessful'
        context['error'] = e.__str__()
        return Response(context)
