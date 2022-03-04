from rest_framework import serializers

from project_management.models import Meeting
from user.serializers import StudentSerializer


class MeetingSerializer(serializers.ModelSerializer):

    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ['link', 'students', 'description', 'date_time']
