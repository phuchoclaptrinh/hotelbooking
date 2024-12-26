from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.models import AbstractBaseUser
from django.forms import ValidationError
from datetime import date
# Create your models here.

class Customer(models.Model):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.user.username
class RoomType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, choices=[('DeluxeDouble','DeluxeDouble'), ('ExecutiveDouble','ExecutiveDouble'), ('JuniorSuiteDouble','JuniorSuiteDouble')]) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
   
    def __str__(self):
        return f"{self.type_name}"

class Room(models.Model):
    '''room_types = [
        ('Deluxe',  'Deluxe'),
        ('Standard', 'Standard'),
        ('Suite', 'Suite'),
    ]'''
    name = models.CharField(max_length=50, unique=True, default=True)
    #type = models.CharField(max_length=20, choices=room_types, default=True)
    room_types = models.ForeignKey(RoomType, on_delete=models.CASCADE, default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    #description = models.TextField(blank=True)
    #is_available = models.BooleanField(default=True)
    #status = models.CharField(max_length=20, choices=[('available', 'Available'), ('booked', 'Booked'), ('maintenance', 'Maintenance')])
    def __str__(self):
        return f"{self.name}-{self.room_types}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Trường customer là ForeignKey liên kết đến model User
    room = models.ForeignKey('Room', on_delete=models.CASCADE)  # Trường room là ForeignKey liên kết đến model Room
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')
    booking_time = models.DateTimeField(auto_now_add=True)
    def clean(self):
        # Kiểm tra ngày check-in và check-out hợp lệ
        if self.check_in_date < date.today():
            raise ValidationError("Ngày check-in phải là hôm nay hoặc muộn hơn.")
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Ngày check-out phải sau ngày check-in.")

        # Kiểm tra nếu phòng đã được đặt trong khoảng thời gian này (chỉ kiểm tra các booking đã xác nhận)
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            status='Confirmed',  # Chỉ kiểm tra các booking đã xác nhận
            check_in_date__lt=self.check_out_date,  # Kiểm tra nếu booking trùng với ngày check-in
            check_out_date__gt=self.check_in_date   # Kiểm tra nếu booking trùng với ngày check-out
        ).exclude(pk=self.pk)  # Loại trừ booking hiện tại (nếu đang cập nhật)
        
        if overlapping_bookings.exists():
            raise ValidationError(f"Phòng {self.room.name} đã được đặt cho những ngày này.")

    def save(self, *args, **kwargs):
        # Gọi phương thức clean() để kiểm tra logic trước khi lưu
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} cho {self.customer.user.username} ({self.check_in_date} - {self.check_out_date})"









    

