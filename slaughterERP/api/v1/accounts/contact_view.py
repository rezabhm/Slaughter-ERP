from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.accounts.models import Contact
from apps.accounts.serializers import ContactSerializers
from utils.rest_framework_class import BaseAPIView


# ---------------- Swagger decorators ----------------
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new contact',
    operation_description='Only admins can create new contacts by providing name and related units.',
    tags=['admin.accounts.contacts'],
    request_body=ContactSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve contact information',
    operation_description='Retrieve a contact by its slug value.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description="Slug of the contact to retrieve.",
            type=openapi.TYPE_STRING
        )
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update contact',
    operation_description='Fully update all contact information.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description="Slug of the contact to update.",
            type=openapi.TYPE_STRING
        )
    ],
    request_body=ContactSerializers,
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update contact',
    operation_description='Update specific fields of a contact.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description="Slug of the contact to partially update.",
            type=openapi.TYPE_STRING
        )
    ],
    request_body=ContactSerializers,
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a contact',
    operation_description='Delete a contact by its slug.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description="Slug of the contact to delete.",
            type=openapi.TYPE_STRING
        )
    ],
    responses={204: 'Contact successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all contacts',
    operation_description='Get a list of all contacts. Supports search by name.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search contacts by name.",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: ContactSerializers(many=True)}
))
class ContactAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing contacts.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ContactSerializers
    lookup_field = 'slug'
    queryset = Contact.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new contact',
    operation_description='everyone can create new contacts by providing name and related units.',
    tags=['accounts.contacts'],
    request_body=ContactSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve contact information',
    operation_description='Retrieve a contact by its slug value.',
    tags=['accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description="Slug of the contact to retrieve.",
            type=openapi.TYPE_STRING
        )
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all contacts',
    operation_description='Get a list of all contacts. Supports search by name.',
    tags=['accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search contacts by name.",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: ContactSerializers(many=True)}
))
class ContactAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing contacts.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ContactSerializers
    lookup_field = 'slug'
    queryset = Contact.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
