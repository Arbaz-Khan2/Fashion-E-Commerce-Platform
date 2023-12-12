from rest_framework import permissions
from .models import CustomUser

class IsAdminOrStaffPermission(permissions.BasePermission):
    """
    Custom permission to allow only admins and staff.
    """

    def has_permission(self, request, view):
        # Check if the user has admin or staff role
        return request.user and request.user.is_authenticated and (
            request.user.role == CustomUser.STAFF or request.user.role == CustomUser.ADMIN
        )

class IsCustomerPermission(permissions.BasePermission):
    """
    Custom permission to allow only customer.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == CustomUser.CUSTOMER
