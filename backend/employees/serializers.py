from django.forms import ValidationError
from rest_framework import serializers
from .models import Employee
from datetime import date
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'