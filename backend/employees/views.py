from django.shortcuts import render

# Create your views here.
# Trong app home/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from home.models import Booking
from home.serializers import BookingSerializer
from django.contrib.auth import get_user_model 
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from .models import Employee
User = get_user_model()
# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number','')
        fullname = request.data.get('fullname', '')
        if not username or not password or not email:
            return Response({
               'detail': 'Usename, password or email are required.' 
            },status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({
                'detail': 'Username already exists.'
            },status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            employee = Employee.objects.create(user=user, phone_number=phone_number, fullname=fullname)
            user.phone_number = phone_number
            user.save()
            employee.save()

            
            return Response({
                'status': 'success',
                'message': 'User registered successfully!',
                'employee_id': user.employee.id,
                'email': user.email,
                'phone_number': employee.phone_number or "N/A",
                'fullname': employee.fullname,
            },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'detail': f'Error: {str(e)}'
            },status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({
                'error': 'Invalid credent'
            },status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({
                'error': 'Invalid credentials.'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = Employee.objects.get(user=user)
            phone_number = employee.phone_number or "N/A"
            fullname = employee.fullname or "N/A"
        except Employee.DoesNotExist:
            # Nếu không tồn tại Customer, trả về thông tin cơ bản
            phone_number = "N/A"

        login(request, user)
        return Response({
            'status': 'success',
            'message': 'Login successful!',
            'employee_id': user.employee.id,
            'email': user.email,
            'phone_number': employee.phone_number or "N/A",
            'fullname': employee.fullname
        }, status=status.HTTP_200_OK)

class AllBookingHistoryView(APIView):
    permission_classes = [IsAuthenticated]  # Chỉ cho phép nhân viên xem

    def get(self, request):
            bookings = Booking.objects.all()  # Lấy tất cả các booking
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)




