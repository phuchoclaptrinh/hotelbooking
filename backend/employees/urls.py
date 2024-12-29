from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views import (AllBookingHistoryView)
from .views import(
    RegisterView, LoginView, EmployeeBookingAPIView, ExampleView
)
from home.views import (
    RoomListView, AvailableRoomListView, BookingCreateView, 
    RoomCreateView, RoomDetailView, RoleCheckView, CheckAvailableRoomsView, AddRoomView, UpdateRoomView, DeleteRoomView
)

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/available/', CheckAvailableRoomsView.as_view(), name='available-room-list'),
    path('bookings/allhistory/', AllBookingHistoryView.as_view(), name='booking-history'),

    path('rooms/add/', RoomCreateView.as_view(), name='add-room'),
    path('rooms/<int:pk>', RoomDetailView.as_view(), name='room-detail'),
    path('role/', RoleCheckView.as_view(), name='role-check'),
    path('login/',LoginView.as_view(), name='login'),
    path('register/',RegisterView.as_view(), name='register'),
    path('add/', AddRoomView.as_view(), name='add_room'),  # API để thêm phòng
    path('update/<int:pk>/', UpdateRoomView.as_view(), name='update_room'),  # API sửa phòng
    path('delete/<int:pk>/', DeleteRoomView.as_view(), name='delete_room'),  # API xóa phòng
    path('bookings/', EmployeeBookingAPIView.as_view(), name='employee-booking'),
    path('example/', ExampleView.as_view(), name='example'),
    ]
