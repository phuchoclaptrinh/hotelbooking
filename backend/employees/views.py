from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from home.models import Booking
from .serializers import BookingSerializer
from django.contrib.auth import get_user_model 
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from .models import Employee
from home.models import Customer
from django.contrib.auth.models import User
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
                'employee_id': employee.id,
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
            'employee_id': employee.id,
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




class EmployeeBookingAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Lấy user_id từ request data
        user_id = request.data.get("user_id")
        room_id = request.data.get("room")
        check_in_date = request.data.get("check_in_date")
        check_out_date = request.data.get("check_out_date")

        # Kiểm tra xem user_id có tồn tại trong request hay không
        if not user_id:
            return Response({"error": "Missing user_id in request data."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer = Customer.objects.filter(id=user_id).first()  # Tìm khách hàng theo id
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Tạo dữ liệu đặt phòng
        serializer = BookingSerializer(data=request.data, context={'request': request})
        
        # Kiểm tra dữ liệu hợp lệ
        if serializer.is_valid():
            # Lưu booking nếu dữ liệu hợp lệ
            serializer.save(customer=customer)  # Gán customer  cho booking
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Trả về lỗi nếu serializer không hợp lệ
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExampleView(APIView):
    def get(self, request):
        customer = Customer.objects.filter(id=1).first()
        if customer:
            return Response({"message": f"Found customer: {customer}"})
        else:
            return Response({"error": "Customer not found!"}, status=404)


