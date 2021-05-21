import json

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import Project, Application
from user.serializers import UserSerializer
from user.permissions import IsFaculty

from student.serializers import AppliedProjectSerializer


from user.models import ACCEPTED, REJECTED, APPPLIED

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsFaculty])
def get_active_projects(request):
    context = {}

    active_projects = Project.objects.filter(
        is_active=True, faculty=request.user.faculty)
    past_projects = Project.objects.filter(
        is_active=False, faculty=request.user.faculty)

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
        applicants = get_user_model().objects.filter(
            student__application__project__uuid_field=project_uuid,
            student__application__project__faculty=request.user.faculty,
            student__application__status=APPPLIED
        )
        project = Project.objects.get(uuid_field=project_uuid)

        serializer = UserSerializer(applicants, many=True)

        context['status'] = 'successful'
        context['title'] = project.title
        context['is_active'] = project.is_active

        context['applications'] = serializer.data

    except:
        context['status'] = 'unsuccessful'

    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsFaculty])
def get_accepted_applicants(request, project_uuid):
    context = {}
    try:
        applicants = get_user_model().objects.filter(
            student__application__project__uuid_field=project_uuid,
            student__application__project__faculty=request.user.faculty,
            student__application__status=ACCEPTED
        )
        project = Project.objects.get(uuid_field=project_uuid)

        serializer = UserSerializer(applicants, many=True)

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
            tags=request.data.get('tags'),
            is_department_specific=request.data.get('is_department_specific'),
            max_students=request.data.get('max_students'),
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date')
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
