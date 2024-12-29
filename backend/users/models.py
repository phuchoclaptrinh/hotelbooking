from django.db import models
from django.contrib.auth.models import User
class Customer(models.Model):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.user.username