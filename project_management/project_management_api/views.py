from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from faculty.serializers import UserApplicationSerializer
from project_management.project_management_api.serializers import MeetingSerializer, TaskSerializer
from project_management.project_management_api.utils import GoogleMananger
from user.models import ACCEPTED, Application, Project, Student


from user.permissions import IsFaculty, IsStudent


from project_management.models import Meeting, Task
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meetings_student(request, project_uuid):
    context = {}

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

        link, event_id = google_manager.create_meeting_link(
            f'{project.faculty.designation}.{project.faculty.user.first_name} {project.faculty.user.last_name}',
            request.data.get('description'),
            request.data.get('start_date'),
            request.data.get('end_date'),
            project.title
        )
        try:

            meeting = Meeting.objects.create(
                link=link,
                project=project,
                date_time=parse_datetime(request.data.get('start_date')),
                description=request.data.get('description')
            )
        except Exception as e:
            google_manager.delete_event(event_id=event_id)
            return Response({'status': 'unsuccessful', 'error': e.__str__()})

        serializer = MeetingSerializer(meeting)
        context['status'] = 'successful'
        context['meeting'] = serializer.data

        google_manager.send_meeting_email(
            [student['value'] for student in request.data.get('students')], meeting, request)

        return Response(context)
    except Exception as e:
        if event_id:
            google_manager.delete_event(event_id)
        context['status'] = 'unsuccessful'
        context['error'] = e.__str__()
        return Response(context)


@api_view(['GET'])
@permission_classes([IsFaculty])
def get_tasks(request, project_uuid):
    try:
        tasks = Task.objects.filter(
            project__uuid_field=project_uuid).order_by('-pk')
        serializer = TaskSerializer(tasks, many=True)

        accepted_applicants = Application.objects.filter(
            project__faculty=request.user.faculty, project__uuid_field=project_uuid, status=ACCEPTED)

        application_serializer = UserApplicationSerializer(
            accepted_applicants, many=True)

        return Response({
            'status': 'successful',
            'tasks': serializer.data,
            'accepted_applications': application_serializer.data
        })

    except Exception as e:
        return Response({'status': 'unsuccessful', 'error': e.__str__()})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def get_tasks_student(request, project_uuid):
    try:
        tasks = Task.objects.filter(
            project__uuid_field=project_uuid).order_by('-pk')
        serializer = TaskSerializer(tasks, many=True)

        return Response({
            'status': 'successful',
            'tasks': serializer.data,
        })

    except Exception as e:
        return Response({'status': 'unsuccessful', 'error': e.__str__()})


@api_view(['POST'])
@permission_classes([IsFaculty])
def change_task_status(request):
    try:
        print(request.data.get('pk'))
        task = Task.objects.get(pk=request.data.get('pk'))
        task.status = request.data.get('status')
        task.save()

        return Response({'status': 'successful'})

    except Exception as e:
        return Response({'status': 'unsuccessful', 'error': e.__str__()})


@api_view(['POST'])
@permission_classes([IsFaculty])
def create_task(request):
    try:
        project = Project.objects.get(
            uuid_field=request.data.get('project_uuid'))
        student = Student.objects.get(
            user__email=request.data.get('student_email'))
        task = Task.objects.create(description=request.data.get(
            'description'), project=project, student=student)

        serializer = TaskSerializer(task)
        return Response({'status': 'successful', 'task': serializer.data})

    except Exception as e:
        return Response({'status': 'unsuccessful', 'error': e.__str__()})
