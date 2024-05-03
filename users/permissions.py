from rest_framework.permissions import BasePermission


class IsOwnerForUser(BasePermission):
    """Permission for user's actions"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsOwnerForTask(BasePermission):
    """Permission for task owner"""
    def has_object_permission(self, request, view, obj):
        return request.user.fio == obj.owner


class IsTaskgiver(BasePermission):
    """Permission for taskgiver's actions"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Taskgiver').exists()


class IsExecutor(BasePermission):
    """Permission for executor's actions"""
    def has_permission(self, request, view):
        return request.user.group.filter(name='Executor').exist()
