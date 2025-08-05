from django.db.models import ProtectedError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import mixins, filters, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.product.models import ProductCategory
from apps.product.serializers import ProductCategorySerializer
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new product category',
    operation_description='Creates a new product category with a unique name and slug. Only accessible to admin users.',
    tags=['admin.product.product_category'],
    request_body=ProductCategorySerializer,
    responses={
        201: ProductCategorySerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a product category',
    operation_description='Retrieves details of a specific product category by its slug. Only accessible to admin users.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product category to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: ProductCategorySerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a product category',
    operation_description='Updates all fields of a product category identified by its slug. Only accessible to admin users.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product category to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=ProductCategorySerializer,
    responses={
        200: ProductCategorySerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a product category',
    operation_description='Updates specific fields of a product category identified by its slug. Only accessible to admin users.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product category to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=ProductCategorySerializer,
    responses={
        200: ProductCategorySerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a product category',
    operation_description='Deletes a product category by its slug. Only accessible to admin users.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product category to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('Product category successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all product categories',
    operation_description='Retrieves a list of all product categories with optional filtering and searching by name or slug. Only accessible to admin users.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search product categories by name or slug.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter product categories by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'slug',
            openapi.IN_QUERY,
            description='Filter product categories by exact slug.',
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: ProductCategorySerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
class ProductCategoryAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for admin-only product category management.
    Supports CRUD operations, filtering, and searching for product categories.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'
    queryset = ProductCategory.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'slug']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('products', 'cars')

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to catch ProtectedError and return meaningful message
        when the category is referenced by existing products.
        """
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            # You can customize the message based on your domain
            return JsonResponse(
                {"detail": "You cannot delete this category because it is assigned to one or more products."},
                status=status.HTTP_409_CONFLICT
            )
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)

@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a product category',
    operation_description='Retrieves details of a specific product category by its slug. Accessible to all users.',
    tags=['product.product_category'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product category to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: ProductCategorySerializer,
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all product categories',
    operation_description='Retrieves a list of all product categories with optional filtering and searching by name or slug. Accessible to all users.',
    tags=['product.product_category'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search product categories by name or slug.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter product categories by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'slug',
            openapi.IN_QUERY,
            description='Filter product categories by exact slug.',
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: ProductCategorySerializer(many=True),
    },
))
class ProductCategoryAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for public access to product categories.
    Supports retrieving and listing product categories with filtering and searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'
    queryset = ProductCategory.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'slug']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('products', 'cars')
