from rest_framework import permissions


class HasAnyPermission(permissions.BasePermission):
    def __init__(self, required_permissions):
        self.required_permissions = required_permissions

    def has_permission(self, request, view):
        # Check if the user has any of the required permissions
        return any(
            request.user.has_perm(permission)
            for permission in self.required_permissions
        )


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow access if the user is a superuser
        if request.user.is_superuser:
            return True

        # Define a mapping of view actions to permission codenames
        action_permissions = {
            "list": "view_user",  # 'list' action requires 'view_user' permission
            "retrieve": "view_user",  # 'retrieve' action requires 'view_user' permission
            "create": "add_user",  # 'create' action requires 'add_user' permission
            "update": "change_user",  # 'update' action requires 'change_user' permission
            "destroy": "delete_user",  # 'destroy' action requires 'delete_user' permission
        }

        # Get the required permission codename for the current action, if any
        required_permission = action_permissions.get(view.action)
        if required_permission:
            # Check if the user is in a group with the required permission
            return request.user.groups.filter(
                permissions__codename=required_permission
            ).exists()

        # Default to not allowing actions not listed in the mapping
        return False
