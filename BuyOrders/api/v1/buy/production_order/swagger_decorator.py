from api.v1.buy.production_order.conf import http_404, http_200
from api.v1.buy.production_order.swagger import VerifiedActionSwagger, ReceivedActionSwagger, FinishedActionSwagger, \
    DoneActionSwagger, CancelledActionSwagger
from apps.buy.serializer import ProductionOrderSerializerPOST, ProductionOrderSerializer
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(

    serializer_class=ProductionOrderSerializerPOST,
    method='bulk_post',
    many=True

)

single_post_request_decorator = custom_swagger_generator(

    serializer_class=ProductionOrderSerializerPOST,
    method='single_post',
    many=False

)

bulk_patch_request_decorator = custom_swagger_generator(

    serializer_class=ProductionOrderSerializer,
    method='bulk_patch',
    many=True

)

single_patch_request_decorator = custom_swagger_generator(

    serializer_class=ProductionOrderSerializer,
    method='single_patch',
    many=False

)

bulk_get_decorator = custom_swagger_generator(

    serializer_class=ProductionOrderSerializer,
    method='bulk_get',
    many=True
)

single_get_decorator = custom_swagger_generator(

    serializer_class=ProductionOrderSerializer,
    method='single_get',
    many=False

)

bulk_delete_request_decorator = custom_swagger_generator(

    serializer_class=ProductionOrderSerializer,
    method='bulk_delete',
    many=True

)

single_delete_request_decorator = custom_swagger_generator(

    serializer_class=ProductionOrderSerializer,
    method='single_delete',
    many=False

)

action_verified_decorator = action_swagger_documentation(

    summaries='set verified status',
    action_name='verified',
    description='set production order to verified or unverified',
    serializer_class=VerifiedActionSwagger,
    res={'200': http_200, '404': http_404}

)

action_received_decorator = action_swagger_documentation(

    summaries='set received status',
    action_name='received',
    description='set production order to received or unreceived',
    serializer_class=ReceivedActionSwagger, res={'200': http_200, '404': http_404}

)

action_finished_decorator = action_swagger_documentation(

    summaries='set finished status',
    action_name='finished',
    description='set production order to finished or unfinished',
    serializer_class=FinishedActionSwagger,
    res={'200': http_200, '404': http_404}

)

action_done_decorator = action_swagger_documentation(

    summaries='set done status',
    action_name='done',
    description='set production order to done and update weight and quality',
    serializer_class=DoneActionSwagger,
    res={'200': http_200, '404': http_404}

)

action_cancelled_decorator = action_swagger_documentation(

    summaries='set cancelled status',
    action_name='cancelled',
    description='set production order to cancelled',
    serializer_class=CancelledActionSwagger, res={'200': http_200}

)