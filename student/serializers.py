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