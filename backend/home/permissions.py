from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):
    """
    Chỉ cho phép nhân viên hoặc admin truy cập.
    """
    def has_permission(self, request, view):
        return request.user.is_staff  # Chỉ cho phép người dùng có quyền admin/staff

