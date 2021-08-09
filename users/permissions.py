from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    message = "Not your account"

    def has_object_permission(self, request, view, obj):
        print(f'running permission: owner is {request.user}')
        return request.user == obj
