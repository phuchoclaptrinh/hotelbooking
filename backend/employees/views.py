from django.shortcuts import render

# Create your views here.
# Trong app home/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from home.models import Booking
from home.serializers import BookingSerializer
from home.permissions import IsEmployee  # Đây là permission kiểm tra nếu người dùng là nhân viên

class AllBookingHistoryView(APIView):
    permission_classes = [IsAuthenticated]  # Chỉ cho phép nhân viên xem

    def get(self, request):
            bookings = Booking.objects.all()  # Lấy tất cả các booking
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)




