from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
        )


class ReadOnlyMe(ReadOnly):

    def has_permission(self, request, view):
        if request.path.split('/')[-2] == 'me':
            return True
        return False


class CreateOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method == 'POST'
        )


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
        )


class ReadOrUpdateOnlyMe(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.path.split('/')[-2] == 'me':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == "PATCH"
        )
