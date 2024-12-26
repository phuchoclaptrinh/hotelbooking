from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Customer, Room, Booking
from .serializers import RoomSerializer, BookingSerializer
from django.core.exceptions import ValidationError
from datetime import datetime
from .forms import RoomForm
# Create your views here
class RoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
class AvailableRoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.filter(is_available=True)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
class BookingCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if not request.user.is_authenticated:
            return Response({"detail": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Khởi tạo và kiểm tra tính hợp lệ của serializer
        serializer = BookingSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Lưu booking nếu dữ liệu hợp lệ
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Trả về lỗi nếu serializer không hợp lệ
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Lấy đối tượng Customer liên kết với User
            customer = request.user.customer
        except Customer.DoesNotExist:
            return Response({"detail": "Customer profile not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Lấy danh sách booking liên quan đến Customer
        bookings = Booking.objects.filter(customer=customer)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomCreateView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_class = [IsAuthenticated]
class RoomDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_class = [IsAuthenticated]
class CheckAvailableRoomsView(APIView):
    def get(self, request):
        check_in_date = request.query_params.get('check_in_date')
        check_out_date = request.query_params.get('check_out_date')

        if not check_in_date or not check_out_date:
            return Response({
                "detail": "Missing parameters. Please provide check_in_date and check_out_date."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra và chuyển đổi ngày tháng sang kiểu Date
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                "detail": "Invalid date format. Expected format: YYYY-MM-DD."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Lọc tất cả các phòng chưa được đặt trong khoảng thời gian này
        available_rooms = Room.objects.filter(
            is_available=True  # Chỉ lấy các phòng có sẵn
        ).exclude(
            id__in=Booking.objects.filter(
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            ).values('room')
        )  # Loại bỏ các phòng đã có booking trong khoảng thời gian

        # Kiểm tra xem có phòng nào còn trống không
        if not available_rooms.exists():
            return Response({
                "detail": "No rooms available for the selected dates."
            }, status=status.HTTP_404_NOT_FOUND)

        # Trả về thông tin các phòng còn trống
        serializer = RoomSerializer(available_rooms, many=True)
        return Response({
            "available_rooms": serializer.data
        })
class RoleCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            return Response({'role': 'employee'})
        else:
            return Response({'role': 'customer'})
        
'''class BookingHistoryView(APIView):
    permission_classes = [IsAuthenticated]  # Chỉ cho phép nhân viên xem

    def get(self, request):
            bookings = Booking.objects.all()  # Lấy tất cả các booking
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)'''
    


# Thêm phòng
class AddRoomView(APIView):
    def post(self, request):
        form = RoomForm(request.data)  # Sử dụng request.data cho API
        if form.is_valid():
            form.save()  # Lưu phòng mới vào cơ sở dữ liệu
            return Response({"message": "Room added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
# Sửa phòng
class UpdateRoomView(APIView):
    def put(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)  # Tìm phòng theo ID
        except Room.DoesNotExist:
            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room, data=request.data)  # Cập nhật thông tin phòng
        if serializer.is_valid():
            serializer.save()  # Lưu thay đổi vào cơ sở dữ liệu
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Xóa phòng
class DeleteRoomView(APIView):
    def delete(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)  # Tìm phòng theo ID
        except Room.DoesNotExist:
            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        room.delete()  # Xóa phòng khỏi cơ sở dữ liệu
        return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
