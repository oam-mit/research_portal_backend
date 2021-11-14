from django.db.models import fields
from rest_framework import serializers

from user.models import Application, Project


class UserApplicationSerializer(serializers.ModelSerializer):

    email = serializers.StringRelatedField(source='student.user.email')
    first_name = serializers.StringRelatedField(
        source='student.user.first_name')
    last_name = serializers.StringRelatedField(
        source='student.user.last_name')
    department = serializers.StringRelatedField(
        source='student.user.department')

    registration_number = serializers.StringRelatedField(
        source='student.registration_number')
    cv = serializers.FileField(source='student.cv')
    domains_of_interest = serializers.StringRelatedField(
        source='student.domains_of_interest')

    class Meta:
        model = Application
        fields = ['email', 'first_name', 'last_name', 'department',
                  'registration_number', 'cv', 'domains_of_interest']
