from typing import List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import View
from apps.core.models import ViewsRoles


def get_methods_roles(view_name: str, method: str) -> List[str]:
    """
    Retrieves allowed roles for a specific view and HTTP method from ViewsRoles model.
    Creates a default entry with 'admin' role if none exists.

    Args:
        view_name (str): The name of the view class.
        method (str): The HTTP method (GET, POST, etc).

    Returns:
        List[str]: List of allowed roles.
    """
    method = method.upper()
    try:
        view_roles = ViewsRoles.objects.get(view_name=view_name, method=method)
        return view_roles.roles
    except ObjectDoesNotExist:
        view_roles = ViewsRoles(view_name=view_name, method=method, roles=['admin'])
        view_roles.save()
        return view_roles.roles


class RoleBasedPermission(BasePermission):
    """
    Permission class that checks user roles from JWT payload against allowed roles
    defined for the view and HTTP method in ViewsRoles.
    """

    def has_permission(self, request: Any, view: View) -> bool:
        """
        Checks if the user has permission to access the view.

        Args:
            request: Incoming HTTP request with JWT payload.
            view: The view instance being accessed.

        Returns:
            bool: True if permission is granted.

        Raises:
            PermissionDenied: If user role is not authorized or token payload is missing.
        """
        payload: Dict[str, Any] = getattr(request, "user_payload", None)
        if not payload:
            raise PermissionDenied("Token payload not found.")

        user_roles: List[Dict[str, str]] = payload.get("roles", [])
        if not user_roles:
            raise PermissionDenied("User role not found in token.")

        method = request.method.upper()
        view_name = view.__class__.__name__
        allowed_roles = get_methods_roles(view_name, method)

        user_role_names = [role['role'] for role in user_roles]
        if any(role in allowed_roles for role in user_role_names):
            return True

        raise PermissionDenied(
            f"Access denied: users with roles {user_role_names} "
            f"are not authorized to perform the '{method}' operation on '{view_name}'."
        )
