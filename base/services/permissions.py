from rest_framework import permissions


class IsModerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return bool(request.user and (request.user.is_moder or request.user.is_superuser))
        except:
            return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return bool(obj.author == request.user or (request.user.is_moder or request.user.is_superuser))
        except:
            try:
                return bool(obj.user == request.user or (request.user.is_moder or request.user.is_superuser))
            except:
                return False

