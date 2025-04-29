from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.product.models import Unit
from apps.product.serializers import UnitSerializers  # Ensure you have this
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new unit',
    operation_description='Only admins can create new units. This operation allows the creation'
                          ' of a new unit with the specified name and slug.',
    tags=['admin.product.unit'],
    request_body=UnitSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a unit by slug',
    operation_description='Retrieve the details of a unit using its slug. This operation requires the slug of'
                          ' the unit.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the unit.", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Update unit (full)',
    operation_description='Fully update the details of a unit using its slug. You need to'
                          ' provide a complete set of updated data for the unit.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the unit.", type=openapi.TYPE_STRING)
    ],
    request_body=UnitSerializers,
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Update unit (partial)',
    operation_description='Partially update the details of a unit using its slug. Only the fields'
                          ' provided in the request will be updated.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the unit.", type=openapi.TYPE_STRING)
    ],
    request_body=UnitSerializers,
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a unit',
    operation_description='Delete a unit from the database using its slug.'
                          ' This operation will remove the unit permanently.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the unit.", type=openapi.TYPE_STRING)
    ],
    responses={204: 'Unit successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all units',
    operation_description='Retrieve a list of all units. You can optionally filter the units by'
                          ' name or slug using the search query parameter.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search units by name or slug.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: UnitSerializers(many=True)}
))
class UnitAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UnitSerializers
    lookup_field = 'slug'
    queryset = Unit.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a unit (public)',
    operation_description='Allow public users to create a unit. Requires unit data to create a new unit.',
    tags=['product.unit'],
    request_body=UnitSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a unit by slug (public)',
    operation_description='Retrieve the details of a unit publicly by its slug.',
    tags=['product.unit'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the unit.", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all units (public)',
    operation_description='Publicly accessible list of all units. You can filter by'
                          ' name or slug with the search query parameter.',
    tags=['product.unit'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search units by name or slug.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: UnitSerializers(many=True)}
))
class UnitAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = UnitSerializers
    lookup_field = 'slug'
    queryset = Unit.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
