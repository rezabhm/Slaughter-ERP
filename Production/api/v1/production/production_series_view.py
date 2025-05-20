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
from apps.production.documents import ProductionSeries, ImportProduct
from utils.custom_api_view import CustomAPIView
from apps.production.serializers.production_series_serializer import ProductionSeriesSerializer
from utils.custom_serializer import CustomSerializer


class TestSerializer(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = '__all__'


class TestAPIView(CustomAPIView):

    model = ProductionSeries
    lookup_field = 'id'
    ordering_fields = '-id'
    serializer_class = {

        'GET': TestSerializer,
        'POST': TestSerializer,
        'PATCH': TestSerializer,
        'PERFORM_ACTION': {

            'test': TestSerializer,
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
        print('run test action')
        return {'message': 'successfully run', 'status': 200}