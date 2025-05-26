from django.utils.decorators import method_decorator

from apps.planning.documents import PlanningSeriesCell
from apps.planning.serializers import PlanningSeriesCellSerializerPOST, PlanningSeriesCellSerializer
from utils.custom_api_view import CustomAPIView
from utils.custom_swagger_generator import custom_swagger_generator


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesCellSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesCellSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesCellSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesCellSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=PlanningSeriesCellSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=PlanningSeriesCellSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesCellSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesCellSerializer, method='single_delete', many=False))
class PlanningSeriesCellAPIView(CustomAPIView):

    model = PlanningSeriesCell
    lookup_field = 'id'
    ordering_fields = ['priority']

    serializer_class = {
        'GET': PlanningSeriesCellSerializer,
        'POST': PlanningSeriesCellSerializerPOST,
        'PATCH': PlanningSeriesCellSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def get_queryset(self):
        return PlanningSeriesCell.objects()