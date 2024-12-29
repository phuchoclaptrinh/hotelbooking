from django.urls import path 
from rest_framework.routers import DefaultRouter

from .views import (
    RoomListView, AvailableRoomListView, BookingCreateView, 
    BookingHistoryView, RoomCreateView, RoomDetailView, RoleCheckView, CheckAvailableRoomsView
)
urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/available/', CheckAvailableRoomsView.as_view(), name='available-room-list'),
    path('bookings/', BookingCreateView.as_view(), name='create-booking'),
    path('bookings/history/', BookingHistoryView.as_view(), name='booking-history'),

    path('rooms/add/', RoomCreateView.as_view(), name='add-room'),
    path('rooms/<int:pk>', RoomDetailView.as_view(), name='room-detail'),
    path('role/', RoleCheckView.as_view(), name='role-check'),

    ]

