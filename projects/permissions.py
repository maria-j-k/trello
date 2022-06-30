from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "Permission denied"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsPO(permissions.BasePermission):
    message = "Permission denied"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.project.owner


class IsAssignedToProject(permissions.BasePermission):
    message = "Permission denied"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or \
                    request.user in obj.coworkers.all()


class IsAssignedToIssue(permissions.BasePermission):
    message = "Permission denied"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or \
                    request.user == obj.assignee
