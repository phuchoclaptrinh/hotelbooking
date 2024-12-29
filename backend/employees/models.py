from django.db import models
from django.contrib.auth.models import User
class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('staff', 'Staff')])
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return f"{self.fullname} ({self.role})"
# Create your models here.
