# from django.utils import timezone
# from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins
#
# from apps.core.documents import DateUser
# from apps.production.documents import ProductionSeries
# from apps.production.serializers.production_series_serializer import ProductionSeriesSerializer
# from utils.jwt_validator import CustomJWTAuthentication
# from utils.post_request import CustomAPIView
# from utils.request_permission import RoleBasedPermission
#
#
# class ProductionSeriesCRUDAPIView(
#
#     GenericViewSet,
#     mixins.CreateModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.ListModelMixin,
#     mixins.DestroyModelMixin
#
# ):
#
#     authentication_classes = [CustomJWTAuthentication]
#     permission_classes = [RoleBasedPermission]
#     serializer_class = ProductionSeriesSerializer
#
#     allowed_roles = {
#
#         'GET': ['admin'],
#         'POST': ['admin'],
#         'PATCH': ['admin'],
#         'PUT': ['admin'],
#         'DELETE': ['admin'],
#
#     }
#
#     # filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#
#     search_fields = [name for name, _ in ProductionSeries._fields.items()]
#     ordering_fields = [name for name in ProductionSeries._fields if 'date' in name.lower()]
#     ordering = 'create_date'
#     # filterset_fields = [name for name, _ in ProductionSeries._fields.items()]
#
#     def get_queryset(self):
#         return ProductionSeries.objects()
#
#
# class ProductionSeriesStartAPIView(CustomAPIView):
#
#     attribute = {
#
#         'start': {
#             'send_required': False,
#             'fun': lambda req, param_post_data: DateUser(user=req.user_payload['username'])
#         },
#         'status': {
#             'send_required': False,
#             'fun': lambda req, param_post_data: 'started'
#
#         }
#
#     }
#
#     allowed_roles = {
#
#         'POST': ['admin'],
#         'GET': ['admin'],
#         'PATCH': ['admin'],
#
#     }
#
#     def get_queryset(self):
#
#         return ProductionSeries.objects()
#
#
# class ProductionSeriesFinishAPIView(CustomAPIView):
#     attribute = {
#
#         'finish': {
#             'send_required': False,
#             'fun': lambda req, param_post_data: timezone.now()
#         },
#
#         'status': {
#             'send_required': False,
#             'fun': lambda req, param_post_data: 'finished'
#
#         }
#
#     }
#
#     allowed_roles = {
#
#         'POST': ['admin'],
#
#     }
#
#     def get_queryset(self):
#         return ProductionSeries.objects()
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from apps.production.documents import ProductionSeries, ImportProduct
from utils.custom_api_view import CustomAPIView
from apps.production.serializers.production_series_serializer import ProductionSeriesSerializer
from utils.custom_serializer import CustomSerializer


class TestSerializer(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = '__all__'


class TestSerializerPOST(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = ['product_owner', 'create']


class SinglePatchSer(serializers.Serializer):
    data = serializers.ListField(
        child=serializers.IntegerField(),
        help_text='List of object IDs to delete'
    )


x = lambda : swagger_auto_schema(
        # method='patch',
        operation_id='bulk_get_production_series',
        request_body=SinglePatchSer,
        responses={
            200: openapi.Response(
                description='Bulk delete result',
                examples={
                    'application/json': {
                        "data": {
                            "1": {"message": "object delete successfully", "status": 200},
                            "2": {"message": "wrong id", "status": 400}
                        }
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid input',
                examples={
                    'application/json': {
                        "message": "you must add data param to your data that must be list of data's id with <id>"
                    }
                }
            )
        },
        operation_summary="Bulk delete objects by ID",
        operation_description="Send a list of IDs to delete multiple objects. "
                              "Returns success or error message for each item individually."
    )

xx = lambda : swagger_auto_schema(
        # method='patch',
        operation_id='bulk_get_productio',
        request_body=SinglePatchSer,
        responses={
            200: openapi.Response(
                description='Bulk delete result',
                examples={
                    'application/json': {
                        "data": {
                            "1": {"message": "object delete successfully", "status": 200},
                            "2": {"message": "wrong id", "status": 400}
                        }
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid input',
                examples={
                    'application/json': {
                        "message": "you must add data param to your data that must be list of data's id with <id>"
                    }
                }
            )
        },
        operation_summary="Bulk delete objects by ID",
        operation_description="Send a list of IDs to delete multiple objects. "
                              "Returns success or error message for each item individually."
    )

@method_decorator(name='single_patch_request', decorator=x())
@method_decorator(name='bulk_patch_request', decorator=xx())
class TestAPIView(CustomAPIView):

    model = ProductionSeries
    lookup_field = 'id'
    ordering_fields = '-id'
    serializer_class = {

        'GET': TestSerializer,
        'POST': TestSerializerPOST,
        'PATCH': TestSerializer,
        'PERFORM_ACTION': {

        },
    }

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],

    }

    def get_queryset(self):

        return self.model.objects()

    def action_test(self, request, data):
        return {'message': 'successfully run', 'status': 200}

    @swagger_auto_schema(
        operation_summary="لیست داده‌ها به صورت گروهی",
        operation_description="این متد برای گرفتن گروهی داده‌ها استفاده می‌شود.",
        responses={200: openapi.Response(description="لیست موفق")},
    )
    def action_verify(self, request, data):
        return {'message': 'successfully run', 'status': 200}
