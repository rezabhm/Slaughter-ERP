from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models.ownership import Agriculture, City
from apps.core.serializers import AgricultureSerializer
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new agriculture record',
    operation_description='Creates a new agriculture entity with a unique name and associated city. Only accessible to admin users.',
    tags=['admin.core.ownership.agriculture'],
    request_body=AgricultureSerializer,
    responses={
        201: AgricultureSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve an agriculture record',
    operation_description='Retrieves details of a specific agriculture entity by its slug. Only accessible to admin users.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the agriculture entity to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: AgricultureSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update an agriculture record',
    operation_description='Updates all fields of an agriculture entity identified by its slug. Only accessible to admin users.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the agriculture entity to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=AgricultureSerializer,
    responses={
        200: AgricultureSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update an agriculture record',
    operation_description='Updates specific fields of an agriculture entity identified by its slug. Only accessible to admin users.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the agriculture entity to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=AgricultureSerializer,
    responses={
        200: AgricultureSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete an agriculture record',
    operation_description='Deletes an agriculture entity by its slug. Only accessible to admin users.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the agriculture entity to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('Agriculture successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all agriculture records',
    operation_description='Retrieves a list of all agriculture entities with optional filtering and searching by name or city. Only accessible to admin users.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search agriculture entities by name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter agriculture entities by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'city',
            openapi.IN_QUERY,
            description='Filter agriculture entities by city ID.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: AgricultureSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='change_city', decorator=swagger_auto_schema(
    operation_summary='Change city for an agriculture record',
    operation_description='Updates the city association for an agriculture entity identified by its slug. Expects a city ID. Only accessible to admin users.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the agriculture entity to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'city_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the city to associate with the agriculture entity.',
            ),
        },
        required=['city_id'],
    ),
    responses={
        200: AgricultureSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid city ID'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Agriculture or city not found.'}}),
    },
))
class AgricultureAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for admin-only management of agriculture entities.
    Supports CRUD operations, city association updates, and filtering/searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = AgricultureSerializer
    lookup_field = 'slug'
    queryset = Agriculture.objects.select_related('city')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'city']
    search_fields = ['name', 'city__name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().select_related('city')

    @action(detail=True, methods=['post'])
    def change_city(self, request, slug=None):
        """
        Update the city association for an agriculture entity.
        """
        agriculture = self.get_object()
        city_id = request.data.get('city_id')

        if not city_id:
            return Response({'detail': 'City ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            city = City.objects.get(id=city_id)
            agriculture.city = city
            agriculture.save()
            serializer = self.get_serializer(agriculture)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except City.DoesNotExist:
            return Response({'detail': 'City not found.'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create an agriculture record',
    operation_description='Creates a new agriculture entity with a unique name and associated city. Accessible to all users.',
    tags=['core.ownership.agriculture'],
    request_body=AgricultureSerializer,
    responses={
        201: AgricultureSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve an agriculture record',
    operation_description='Retrieves details of a specific agriculture entity by its slug. Accessible to all users.',
    tags=['core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the agriculture entity to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: AgricultureSerializer,
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all agriculture records',
    operation_description='Retrieves a list of all agriculture entities with optional filtering and searching by name or city. Accessible to all users.',
    tags=['core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search agriculture entities by name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter agriculture entities by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'city',
            openapi.IN_QUERY,
            description='Filter agriculture entities by city ID.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: AgricultureSerializer(many=True),
    },
))
class AgricultureAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for public access to agriculture entities.
    Supports creating, retrieving, and listing agriculture entities with filtering and searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = AgricultureSerializer
    lookup_field = 'slug'
    queryset = Agriculture.objects.select_related('city')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'city']
    search_fields = ['name', 'city__name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().select_related('city')