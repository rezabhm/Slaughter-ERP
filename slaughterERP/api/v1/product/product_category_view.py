from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.product.models import ProductCategory
from apps.product.serializers import ProductCategorySerializer
from utils.rest_framework_class import BaseAPIView


# ---------------- Admin API View ----------------
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new product category',
    operation_description='Only admins can create new product categories. This operation '
                          'allows the creation of a new product category with the specified name and slug.',
    tags=['admin.product.product_category'],
    request_body=ProductCategorySerializer,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a product category by slug',
    operation_description='Retrieve the details of a product category using its slug.'
                          ' This operation requires the slug of the product category.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product category.",
                          type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Update product category (full)',
    operation_description='Fully update the details of a product category using its slug. You need to provide a'
                          ' complete set of updated data for the product category.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product category.",
                          type=openapi.TYPE_STRING)
    ],
    request_body=ProductCategorySerializer,
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Update product category (partial)',
    operation_description='Partially update the details of a product category using its slug. '
                          'Only the fields provided in the request will be updated.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product category.",
                          type=openapi.TYPE_STRING)
    ],
    request_body=ProductCategorySerializer,
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a product category',
    operation_description='Delete a product category from the database using its slug.'
                          ' This operation will remove the product category permanently.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product category.",
                          type=openapi.TYPE_STRING)
    ],
    responses={204: 'Product category successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all product categories',
    operation_description='Retrieve a list of all product categories. You can optionally filter'
                          ' the categories by name or slug using the search query parameter.',
    tags=['admin.product.product_category'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search product categories by name or slug.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: ProductCategorySerializer(many=True)}
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'
    queryset = ProductCategory.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']


@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a product category by slug (public)',
    operation_description='Retrieve the details of a product category publicly by its slug.',
    tags=['product.product_category'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product category.",
                          type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all product categories (public)',
    operation_description='Publicly accessible list of all product categories. '
                          'You can filter by name or slug with the search query parameter.',
    tags=['product.product_category'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search product categories by name or slug.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: ProductCategorySerializer(many=True)}
))
class ProductCategoryAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'
    queryset = ProductCategory.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
