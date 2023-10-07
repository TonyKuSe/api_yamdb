from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_admin or request.method
            in permissions.SAFE_METHODS
        )


class ReadOrUpdateOnlyMe(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.path.endswith('me/')

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'PATCH'
        )


class NotUpdateMeRole(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            not (
                request.method == 'PATCH'
                and request.path.endswith('me/')
                and 'role' in request.data
            )
        )


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user == obj.author
                or request.user.is_admin
                or request.user.is_moderator
            )
        )
