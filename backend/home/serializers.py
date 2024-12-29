from django.forms import ValidationError
from rest_framework import serializers
from .models import Customer, Room, Booking
from datetime import date


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'



class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id', read_only=True)  # Thêm idbooking
    user_id = serializers.IntegerField(source='customer.id', read_only=True)  # Thêm iduser
    

    class Meta:
        model = Booking
        fields = ['booking_id' , 'user_id' , 'room', 'check_in_date', 'check_out_date', 'status', 'booking_time']  # Thêm các trường mới
        read_only_fields = ['customer']  # 'customer' sẽ được gán tự động trong view

    def create(self, validated_data):
        # Lấy user hiện tại từ request context
        user = self.context['request'].user
        
        # Lấy hoặc tạo đối tượng Customer từ user
        customer, created = Customer.objects.get_or_create(user=user)

        # Gán customer vào validated_data trước khi tạo Booking
        validated_data['customer'] = customer

        # Tạo và trả về đối tượng Booking
        return Booking.objects.create(**validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'



#class BookingSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = Booking
        #fields = ['id', 'room', 'check_in_date', 'check_out_date', 'status']  # Chọn các trường cần trả về

    #def to_representation(self, instance):
        """
        Tùy chỉnh cách dữ liệu được trả về.
        Ví dụ: có thể thêm tên phòng vào thay vì chỉ trả về id.
        """
        #representation = super().to_representation(instance)
        #representation['room_name'] = instance.room.name  # Thêm tên phòng vào kết quả
        #return representation

        