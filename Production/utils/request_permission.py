
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class RoleBasedPermission(BasePermission):
    """
    Checks if the user role from JWT payload is allowed to access
    the current method (GET, POST, etc.), using rules defined in the view.
    """

    def has_permission(self, request, view):
        # Extract user role from JWT payload
        payload = getattr(request, "user_payload", None)

        if not payload:
            raise PermissionDenied("Token payload not found.")

        user_role = payload.get("roles")

        if not user_role:
            raise PermissionDenied("User role not found in token.")

        # Get the request method (e.g., GET, POST)
        method = request.method.upper()

        # Get allowed roles per method from the view
        allowed_roles = getattr(view, "allowed_roles", {})

        # Get the list of roles allowed for this method
        roles_for_method = allowed_roles.get(method, [])

        for role in roles_for_method:
            if role == 'any':
                return True

        for role in user_role:
            if role['role'] in roles_for_method:
                return True

        raise PermissionDenied(f"Role '{user_role}' is not allowed to perform '{method}' operation.")
