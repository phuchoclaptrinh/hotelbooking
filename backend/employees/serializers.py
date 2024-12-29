from django.forms import ValidationError
from rest_framework import serializers
from .models import Employee
from datetime import date
from home.models import Booking, Customer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id', read_only=True)
    user_id = serializers.IntegerField(source='customer.id', read_only=True)

    class Meta:
        model = Booking
        fields = ['booking_id', 'user_id', 'room', 'check_in_date', 'check_out_date', 'status', 'booking_time']
        read_only_fields = ['customer']

    def create(self, validated_data):
        # Lấy user hiện tại từ request context (user đã đăng nhập)
        user = self.context['request'].user

        # Lấy customer_id từ dữ liệu request (tức là user_id)
        customer_id = self.context['request'].data.get('user_id')

        # Lấy đối tượng Customer từ customer_id
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer not found.")

        # Gán customer vào validated_data trước khi tạo Booking
        validated_data['customer'] = customer

        # Tạo đối tượng Booking và lưu vào cơ sở dữ liệu
        booking = Booking.objects.create(**validated_data)

        # Trả về đối tượng đã được tạo
        return booking


