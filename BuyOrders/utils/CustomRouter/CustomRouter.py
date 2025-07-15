from typing import List, Type, Any
from django.urls import path
from rest_framework.views import APIView


class CustomRouter:
    """
    Custom router for registering Django URL patterns for RESTful API views.
    Supports bulk and single operations, as well as custom actions.
    """

    def __init__(self) -> None:
        """Initialize the router with an empty list of URL patterns."""
        self.urls: List[Any] = []

    def register(self, url: str, view: Type[APIView]) -> None:
        """
        Register URL patterns for the given view class.

        Args:
            url: Base URL path for the view (e.g., 'items').
            view: The APIView class to register.
            name: Optional name for the URL pattern (not used currently).

        Returns:
            None: Adds URL patterns to the internal urls list.
        """
        # Ensure URL ends with a trailing slash
        url = url.rstrip('/') + '/'

        # Instantiate view to access its methods
        view_instance = view()

        # Get custom action methods from the view
        action_list = view_instance.get_action_fun_list()

        # Register URL patterns for bulk operations
        self.urls.append(
            path(url, view.as_view({
                'get': 'bulk_get',
                'post': 'bulk_post_request',
                'patch': 'bulk_patch_request',
                'delete': 'bulk_delete_request',
            }))
        )

        # Register URL patterns for single operations
        self.urls.append(
            path(f'{url}<str:slug_field>/', view.as_view({
                'get': 'single_get',
                'patch': 'single_patch_request',
                'delete': 'single_delete_request',
            }))
        )

        # Register URL pattern for single POST operation
        self.urls.append(
            path(f'{url}create/', view.as_view({
                'post': 'single_post_request',
            }))
        )

        # Register URL patterns for custom actions
        for action_name in action_list:
            self.urls.append(
                path(f'{url}<str:slug>/{action_name}/', view.as_view({
                    'post': f'action_{action_name}',
                }))
            )
