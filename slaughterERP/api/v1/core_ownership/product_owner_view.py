from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models.ownership import ProductOwner
from apps.core.serializers import ProductOwnerSerializers
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new product owner',
    operation_description='Only admins can create product owners by providing contact info.',
    tags=['admin.core.ownership.product_owner'],
    request_body=ProductOwnerSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve product owner details',
    operation_description='Retrieve a product owner by their slug.',
    tags=['admin.core.ownership.product_owner'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product owner", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a product owner',
    operation_description='Admins can fully update product owner info.',
    tags=['admin.core.ownership.product_owner'],
    request_body=ProductOwnerSerializers,
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product owner", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update product owner',
    operation_description='Admins can partially update product owner info.',
    tags=['admin.core.ownership.product_owner'],
    request_body=ProductOwnerSerializers,
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product owner", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a product owner',
    operation_description='Admins can delete product owners by slug.',
    tags=['admin.core.ownership.product_owner'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product owner", type=openapi.TYPE_STRING)
    ],
    responses={204: 'Product owner successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all product owners',
    operation_description='List of all product owners with optional search by contact name.',
    tags=['admin.core.ownership.product_owner'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search by contact name", type=openapi.TYPE_STRING)
    ],
    responses={200: ProductOwnerSerializers(many=True)}
))
class ProductOwnerAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing product owners.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductOwnerSerializers
    lookup_field = 'slug'
    queryset = ProductOwner.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['contact__name']


# ---------------- Swagger decorators for Public ----------------
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a product owner',
    operation_description='Anyone can create a product owner by providing contact info.',
    tags=['core.ownership.product_owner'],
    request_body=ProductOwnerSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve product owner details',
    operation_description='Retrieve a product owner by slug.',
    tags=['core.ownership.product_owner'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the product owner", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all product owners',
    operation_description='List all product owners with search by contact name.',
    tags=['core.ownership.product_owner'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search by contact name", type=openapi.TYPE_STRING)
    ],
    responses={200: ProductOwnerSerializers(many=True)}
))
class ProductOwnerAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Public API ViewSet for viewing and creating product owners.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = ProductOwnerSerializers
    lookup_field = 'slug'
    queryset = ProductOwner.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['contact__name']
