from typing import List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import View
from apps.core.models import ViewsRoles


def get_methods_roles(view_name: str, method: str) -> List[str]:
    """
    Retrieves the allowed roles for a specific view and HTTP method from the ViewsRoles model.
    If no roles are defined, creates a default entry with 'admin' role and saves it.

    Args:
        view_name (str): Name of the view class.
        method (str): HTTP method (e.g., GET, POST).

    Returns:
        List[str]: List of roles allowed for the view and method.

    Raises:
        ObjectDoesNotExist: If the ViewsRoles object does not exist (handled internally).
    """
    method = method.upper()  # Normalize HTTP method to uppercase
    try:
        # Attempt to retrieve the ViewsRoles object for the given view and method
        view_roles = ViewsRoles.objects.get(view_name=view_name, method=method)
        return view_roles.roles
    except ObjectDoesNotExist:
        # If no roles are defined, create a default entry with 'admin' role
        view_roles = ViewsRoles(
            view_name=view_name,
            method=method,
            roles=['admin']  # Default role; consider making this configurable
        )
        view_roles.save()
        return view_roles.roles


class RoleBasedPermission(BasePermission):
    """
    A custom permission class that checks if the user's role from the JWT payload
    is authorized to perform the requested HTTP method on the given view, based on
    roles defined in the ViewsRoles model.
    """

    def has_permission(self, request: Any, view: View) -> bool:
        """
        Determines if the user has permission to perform the requested action.

        Args:
            request: The incoming HTTP request containing the JWT payload.
            view: The view instance being accessed.

        Returns:
            bool: True if the user is authorized, False otherwise.

        Raises:
            PermissionDenied: If the user lacks the required role or token data is invalid.
        """
        # Extract user payload from JWT
        payload: Dict[str, Any] = getattr(request, "user_payload", None)
        if not payload:
            raise PermissionDenied("Token payload not found.")

        # Extract user roles from payload
        user_roles: List[Dict[str, str]] = payload.get("roles", [])
        if not user_roles:
            raise PermissionDenied("User role not found in token.")

        # Get the HTTP method (e.g., GET, POST)
        method: str = request.method.upper()

        # Retrieve allowed roles for the view and method
        view_name: str = view.__class__.__name__
        allowed_roles: List[str] = get_methods_roles(view_name, method)

        # Check if any of the user's roles are in the allowed roles
        user_role_names: List[str] = [role['role'] for role in user_roles]
        for role in user_role_names:
            if role in allowed_roles:
                return True

        # Raise PermissionDenied with a clear error message
        raise PermissionDenied(
            f"Access denied: users with roles {user_role_names} "
            f"are not authorized to perform the '{method}' operation on '{view_name}'."
        )