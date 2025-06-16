from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.product.models import Product
from apps.product.serializers import ProductSerializer  # Ensure you have this
from utils.rest_framework_class import BaseAPIView


# ---------------- Admin API View ----------------
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new product',
    operation_description='Only admins can create new products. This operation allows admins to create'
                          ' products with specific name, code, category, and unit information.',
    tags=['admin.product.product'],
    request_body=ProductSerializer,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a product by slug',
    operation_description='Retrieve the details of a product by its slug. You need to provide the slug of the product.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product.", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Update product (full)',
    operation_description='Fully update the details of a product using its slug. You need to provide '
                          'the complete set of updated data for the product.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product.", type=openapi.TYPE_STRING)
    ],
    request_body=ProductSerializer,
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Update product (partial)',
    operation_description='Partially update the details of a product using its slug. Only the fields'
                          ' provided in the request will be updated.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product.", type=openapi.TYPE_STRING)
    ],
    request_body=ProductSerializer,
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a product',
    operation_description='Delete a product from the database using its slug. '
                          'This operation will remove the product permanently.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product.", type=openapi.TYPE_STRING)
    ],
    responses={204: 'Product successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all products',
    operation_description='Retrieve a list of all products. You can optionally filter the products by name, code,'
                          ' category, or unit using the search query parameter.',
    tags=['admin.product.product'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search products by name, "
                                                                  "code, category, or unit.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: ProductSerializer(many=True)}
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'category__name', 'unit__name']


@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a product by slug (public)',
    operation_description='Publicly accessible operation to retrieve a product by its slug.',
    tags=['product.product'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product.", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all products (public)',
    operation_description='Publicly accessible operation to list all products. You can filter products by name, code, '
                          'category, or unit using the search query parameter.',
    tags=['product.product'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search products "
                                                                  "by name, code, category, or unit.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: ProductSerializer(many=True)}
))
class ProductAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'category__name', 'unit__name']
