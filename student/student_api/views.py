from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from user.serializers import DepartmentSerializer
from user.models import Department,Project,Application
from user.permissions import IsStudent

from ..serializers import ProjectSerializer,AppliedProjectSerializer,ApplicationSerializer

from user.serializers import UserSerializer
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStudent])
def get_departments(request):
    context={}
    departments=Department.objects.all()
    serializer=DepartmentSerializer(departments,many=True)
    context['departments']=serializer.data

    return Response(context)

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStudent])
def get_projects(request,department_slug):
    context={}
    try:
        department=Department.objects.get(slug=department_slug)
    except:
        context['status']='slug does not exist'
        return Response(context)
    submitted_applications=Application.objects.filter(student=request.user.student)
    projects=Project.objects.filter(faculty__user__department__slug=department_slug)

    if department_slug!=request.user.department.slug:
        projects=projects.exclude(is_department_specific=True)
        
    serializer=ProjectSerializer(projects,many=True,context={'user':request.user})
    context['status']='ok'
    context['projects']=serializer.data
    context['department_name']=department.name


    return Response(context)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsStudent])
def submit_application(request):
    context={}
    try:
        project=Project.objects.get(uuid_field=request.data.get('project_uuid_field'))
        application=Application.objects.create(
            project=project,student=request.user.student
        )
        context['status']='successful'
    except ObjectDoesNotExist:
        context['status']='unsuccessful'
        context['error']='UUID Invalid'
    except IntegrityError:
        context['status']='unuccesful'
        context['error']='Already Submitted'
    
    return Response(context)

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStudent])
def check_submitted(request):
    context={}
    try:
        Application.objects.get(project__uuid_field=request.GET.get('project_uuid_field'),student=request.user.student)
        context['status']='submitted'
    except:
        context['status']='not submitted'
    return Response(context)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsStudent])
def update_profile(request):
    pass

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStudent])
def get_applied_projects(request):
    context={}
    applications=Application.objects.filter(student=request.user.student)
    serializer=ApplicationSerializer(applications,many=True)
    context['projects']=serializer.data

    return Response(context)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsStudent])
def submit_cv(request):
    context={}
    try:
        request.user.student.cv=request.FILES.get('cv')
        request.user.student.save()
        serializer=UserSerializer(request.user)
        context['status']='successful'
        context['user']=serializer.data
        return Response(context)
    except Exception as e:
        context['status']='unsuccessful'
        context['error']=e.__str__()
        print(context)
        return Response(context)



