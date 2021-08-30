from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import empty

from .models import Feedback, User, Student, Department, Project, Application


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['registration_number', 'cv']


class UserSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    registration_number = serializers.CharField(
        source='student.registration_number')
    cv = serializers.FileField(source='student.cv')
    profile_picture = serializers.ImageField(source='faculty.profile_picture')
    designation = serializers.CharField(source='faculty.designation')
    domains_of_interest = serializers.CharField(
        source='student.domains_of_interest')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'department', 'is_student',
                  'is_faculty', 'registration_number', 'cv', 'domains_of_interest', 'profile_picture', 'designation']

    def to_representation(self, instance):
        if instance.is_student:
            try:
                self.fields.pop('profile_picture')
                self.fields.pop('designation')
            except Exception as e:
                print(e)
        else:
            try:
                self.fields.pop('cv')
                self.fields.pop('domains_of_interest')
                self.fields.pop('registration_number')
            except Exception as e:
                print(e)
        return super().to_representation(instance)


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['name', 'department_building', 'slug']


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['project_is_complete', 'feedback']
