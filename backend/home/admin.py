from django.contrib import admin
from .models import Room, Booking, Employee, RoomType
# Register your models here.
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Employee)
admin.site.register(RoomType)
