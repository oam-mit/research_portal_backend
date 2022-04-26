import json
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from faculty.serializers import UserApplicationSerializer

from user.models import Project, Application, Feedback
from user.serializers import FeedbackSerializer, UserSerializer
from user.permissions import IsFaculty

from student.serializers import AppliedProjectSerializer

from ..utils import FacultyEmail


from user.models import ACCEPTED, REJECTED, APPPLIED

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsFaculty])
def get_active_projects(request):
    context = {}

    active_projects = Project.objects.filter(
        is_active=True, faculty=request.user.faculty).order_by('-start_date')
    past_projects = Project.objects.filter(
        is_active=False, faculty=request.user.faculty).order_by('-start_date')

    active_project_serializer = AppliedProjectSerializer(
        active_projects, many=True)
    past_project_serializer = AppliedProjectSerializer(
        past_projects, many=True)

    context['active_projects'] = active_project_serializer.data
    context['past_projects'] = past_project_serializer.data

    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsFaculty])
def get_applicants(request, project_uuid):
    context = {}
    try:
        applicants = Application.objects.filter(
            project__faculty=request.user.faculty, project__uuid_field=project_uuid)
        count_accepted = applicants.filter(status=ACCEPTED).count()
        applicants = applicants.filter(status=APPPLIED)
        project = Project.objects.get(uuid_field=project_uuid)
        print(applicants)
        serializer = UserApplicationSerializer(applicants, many=True)

        context['status'] = 'successful'
        context['title'] = project.title
        context['is_active'] = project.is_active
        context['count_accepted'] = count_accepted
        context['count_max'] = project.max_students

        context['applications'] = serializer.data

    except Exception as e:
        print(e.__str__())
        context['status'] = 'unsuccessful'

    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsFaculty])
def get_accepted_applicants(request, project_uuid):
    context = {}
    try:
        applicants = Application.objects.filter(
            project__faculty=request.user.faculty, project__uuid_field=project_uuid, status=ACCEPTED)

        project = Project.objects.get(uuid_field=project_uuid)

        serializer = UserApplicationSerializer(applicants, many=True)

        context['status'] = 'successful'
        context['title'] = project.title

        context['applications'] = serializer.data

    except:
        context['status'] = 'unsuccessful'

    return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsFaculty])
def submit_project(request):
    context = {}

    try:
        project = Project.objects.create(
            faculty=request.user.faculty,
            title=request.data.get('title'),
            description=request.data.get('description'),
            outcome=request.data.get('outcome'),
            tags=request.data.get('tags'),
            is_department_specific=request.data.get('is_department_specific'),
            is_extendable=request.data.get('is_extendable'),
            max_students=request.data.get('max_students'),
            hours_per_week=request.data.get('hours_per_week'),
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date'),

        )
        context['status'] = 'successful'
        return Response(context)
    except Exception as e:
        context['status'] = 'unsuccessful'
        context['error'] = e.__str__()
        return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsFaculty])
def update_profile_picture(request):
    context = {}
    try:
        request.user.faculty.profile_picture = request.FILES.get(
            'profile_picture')
        request.user.faculty.save()
        serializer = UserSerializer(request.user)
        context['status'] = 'successful'
        context['user'] = serializer.data
        return Response(context)
    except Exception as e:
        context['status'] = 'unsuccessful'
        context['error'] = e.__str__()
        print(context)
        return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsFaculty])
def application_change_status(request):
    context = {}
    try:
        application = Application.objects.get(
            project__uuid_field=request.data.get('uuid_field'),
            student__user__email=request.data.get('student_email')
        )

        application.status = request.data.get('status')
        application.save()

        context['status'] = 'successful'

        FacultyEmail().send_application_status_change_email(request, application)

    except:
        context['status'] = 'unsuccessful'
        context['error'] = 'wrong data'

    return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsFaculty])
def change_project_status(request):
    context = {}
    try:
        project = Project.objects.get(
            uuid_field=request.data.get('uuid_field'))
        project.is_active = not project.is_active
        project.save()
        context['status'] = 'successful'
        return Response(context)
    except Exception as e:
        context['status'] = 'unsuccessful'
        context['error'] = e.__str__()
        print(e.__str__())

    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsFaculty])
def check_feedback_submitted(request, project_uuid, email):
    try:
        feedback = Feedback.objects.get(
            application__project__uuid_field=project_uuid,
            application__student__user__email=email
        )
        return Response({
            'status': 'submitted',
            'feedback': FeedbackSerializer(feedback).data
        })
    except:
        return Response({
            'status': 'not submitted'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsFaculty])
def submit_feedback(request):
    try:
        application = Application.objects.get(
            project__uuid_field=request.data.get('project_uuid'),
            student__user__email=request.data.get('email')
        )
        Feedback.objects.create(
            application=application,
            project_is_complete=request.data.get('project_is_complete'),
            feedback=request.data.get('feedback')
        )
        return Response({
            'status': 'successful'
        })
    except:
        return Response({
            'status': 'unsuccessful',
            'error': 'Wrong email and uuid'
        })
