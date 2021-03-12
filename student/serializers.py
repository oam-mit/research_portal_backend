from rest_framework import serializers

from user.models import Project,Application
from user.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    faculty=UserSerializer(many=False,read_only=True,source='faculty.user')
    applied=serializers.SerializerMethodField()
    class Meta:
        model=Project
        fields=['uuid_field','title','description','faculty','applied','tags','max_students','start_date','end_date','is_active']
    
    def get_applied(self,obj):
        applications=Application.objects.filter(project=obj,student=self.context['user'].student)

        if applications.exists():
            return True
        else:
            return False

class AppliedProjectSerializer(serializers.ModelSerializer):
    department_slug=serializers.CharField(source='faculty.user.department.slug',)
    faculty=UserSerializer(many=False,read_only=True,source='faculty.user')
    class Meta:
        model=Project
        fields=['uuid_field','title','start_date','end_date','faculty','department_slug']
    

class ApplicationSerializer(serializers.ModelSerializer):
    uuid_field=serializers.CharField(source='project.uuid_field')
    title=serializers.CharField(source='project.title')
    start_date=serializers.DateField(source='project.start_date')
    end_date=serializers.DateField(source='project.end_date')
    faculty=UserSerializer(many=False,read_only=True,source='project.faculty.user')
    department_slug=serializers.CharField(source='project.faculty.user.department.slug')

    class Meta:
        model=Application
        fields=['uuid_field','title','start_date','end_date','faculty','department_slug','status']