from rest_framework import permissions

class CreateWardUser(permissions.BasePermission):
    message = "creating ward level user is not allowed"