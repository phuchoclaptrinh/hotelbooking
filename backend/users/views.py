from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model 
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from home.models import Customer
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
            customer = Customer.objects.create(user=user, phone_number=phone_number, fullname=fullname)
            user.phone_number = phone_number
            user.save()
            customer.save()

            
            return Response({
                'status': 'success',
                'message': 'User registered successfully!',
                'user_id': user.id,
                'email': user.email,
                'phone_number': customer.phone_number or "N/A",
                'fullname': customer.fullname,
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
            customer = Customer.objects.get(user=user)
            phone_number = customer.phone_number or "N/A"
            fullname = customer.fullname or "N/A"
        except Customer.DoesNotExist:
            # Nếu không tồn tại Customer, trả về thông tin cơ bản
            phone_number = "N/A"

        login(request, user)
        return Response({
            'status': 'success',
            'message': 'Login successful!',
            'user_id': user.id,
            'email': user.email,
            'phone_number': customer.phone_number or "N/A",
        }, status=status.HTTP_200_OK)

