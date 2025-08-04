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

from apps.product.models import Product, ProductCategory, Unit
from apps.product.serializers import ProductSerializer
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new product',
    operation_description='Creates a new product with a unique name, code, category, and unit. Only accessible to admin users.',
    tags=['admin.product.product'],
    request_body=ProductSerializer,
    responses={
        201: ProductSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a product',
    operation_description='Retrieves details of a specific product by its slug. Only accessible to admin users.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: ProductSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a product',
    operation_description='Updates all fields of a product identified by its slug. Only accessible to admin users.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=ProductSerializer,
    responses={
        200: ProductSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a product',
    operation_description='Updates specific fields of a product identified by its slug. Only accessible to admin users.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=ProductSerializer,
    responses={
        200: ProductSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a product',
    operation_description='Deletes a product by its slug. Only accessible to admin users.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('Product successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all products',
    operation_description='Retrieves a list of all products with optional filtering and searching by name, code, category, or unit. Only accessible to admin users.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search products by name, code, category name, or unit name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter products by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'code',
            openapi.IN_QUERY,
            description='Filter products by exact code.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'category',
            openapi.IN_QUERY,
            description='Filter products by category ID.',
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            'unit',
            openapi.IN_QUERY,
            description='Filter products by unit ID.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: ProductSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='change_category', decorator=swagger_auto_schema(
    operation_summary='Change category for a product',
    operation_description='Updates the category association for a product identified by its slug. Expects a category ID. Only accessible to admin users.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the category to associate with the product.',
            ),
        },
        required=['category_id'],
    ),
    responses={
        200: ProductSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid category ID'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Product or category not found.'}}),
    },
))
@method_decorator(name='change_unit', decorator=swagger_auto_schema(
    operation_summary='Change unit for a product',
    operation_description='Updates the unit association for a product identified by its slug. Expects a unit ID. Only accessible to admin users.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'unit_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the unit to associate with the product.',
            ),
        },
        required=['unit_id'],
    ),
    responses={
        200: ProductSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid unit ID'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Product or unit not found.'}}),
    },
))
class ProductAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for admin-only product management.
    Supports CRUD operations, category and unit association updates, and filtering/searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    queryset = Product.objects.select_related('category', 'unit')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'code', 'category', 'unit']
    search_fields = ['name', 'code', 'category__name', 'unit__name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().select_related('category', 'unit')

    @action(detail=True, methods=['post'])
    def change_category(self, request, slug=None):
        """
        Update the category association for a product.
        """
        product = self.get_object()
        category_id = request.data.get('category_id')

        if not category_id:
            return Response({'detail': 'Category ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = ProductCategory.objects.get(id=category_id)
            product.category = category
            product.save()
            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductCategory.DoesNotExist:
            return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def change_unit(self, request, slug=None):
        """
        Update the unit association for a product.
        """
        product = self.get_object()
        unit_id = request.data.get('unit_id')

        if not unit_id:
            return Response({'detail': 'Unit ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            unit = Unit.objects.get(id=unit_id)
            product.unit = unit
            product.save()
            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Unit.DoesNotExist:
            return Response({'detail': 'Unit not found.'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a product',
    operation_description='Retrieves details of a specific product by its slug. Accessible to all users.',
    tags=['product.product'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the product to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: ProductSerializer,
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all products',
    operation_description='Retrieves a list of all products with optional filtering and searching by name, code, category, or unit. Accessible to all users.',
    tags=['product.product'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search products by name, code, category name, or unit name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter products by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'code',
            openapi.IN_QUERY,
            description='Filter products by exact code.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'category',
            openapi.IN_QUERY,
            description='Filter products by category ID.',
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            'unit',
            openapi.IN_QUERY,
            description='Filter products by unit ID.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: ProductSerializer(many=True),
    },
))
class ProductAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for public access to products.
    Supports retrieving and listing products with filtering and searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    queryset = Product.objects.select_related('category', 'unit')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'code', 'category', 'unit']
    search_fields = ['name', 'code', 'category__name', 'unit__name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().select_related('category', 'unit')