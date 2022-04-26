from rest_framework import serializers

from project_management.models import Meeting, Task
from user.serializers import StudentSerializer, UserSerializer


class MeetingSerializer(serializers.ModelSerializer):

    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ['link', 'students', 'description', 'date_time']


class TaskSerializer(serializers.ModelSerializer):
    student = UserSerializer(source='student.user')

    class Meta:
        model = Task
        fields = ['student', 'status', 'description', 'pk']
