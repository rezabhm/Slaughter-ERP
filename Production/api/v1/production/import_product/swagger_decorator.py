from api.v1.production.import_product.conf import *
from api.v1.production.import_product.swagger import *
from apps.production.serializers.import_product_serializer import (
    ImportProductSerializer,
    ImportProductSerializerPOST,
    ImportProductFromWareHouseSerializer,
    ImportProductFromWareHouseSerializerPOST,
)
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

# ImportProductByCarAPIView decorators
bulk_post_request_decorator = custom_swagger_generator(serializer_class=ImportProductSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=ImportProductSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_delete', many=False)
action_planned_decorator = action_swagger_documentation(
    summaries='Plan the Import Product',
    action_name='planned',
    description='Plan the import product by updating the status to "planned".',
    serializer_class=IsStatusSwaggerSerializer,
    res={'200': is_status_dict['is_planned']},
)
action_cancel_decorator = action_swagger_documentation(
    summaries='Cancel the Import Product',
    action_name='cancel',
    description='Cancel the import product by updating the status to "cancelled".',
    serializer_class=IsStatusSwaggerSerializer,
    res={'200': is_status_dict['is_cancelled']},
)
action_verify_decorator = action_swagger_documentation(
    summaries='Verify the Import Product',
    action_name='verify',
    description='Verify the import product by updating the status to "verified".',
    serializer_class=IsStatusSwaggerSerializer,
    res={'200': is_status_dict['is_verified']},
)
action_first_step_decorator = action_swagger_documentation(
    summaries='Step 1: Entrance to Slaughter',
    action_name='first_step',
    description='Record entrance to slaughter time.',
    serializer_class=FirstStepSwaggerSerializer,
    res={'200': steps_data[1]['status']},
)
action_second_step_decorator = action_swagger_documentation(
    summaries='Step 2: Weight and Cage Details',
    action_name='second_step',
    description='Register full weight, source weight, cage number, and number of products per cage.',
    serializer_class=SecondStepSwaggerSerializer,
    res={'200': steps_data[2]['status']},
)
action_third_step_decorator = action_swagger_documentation(
    summaries='Step 3: Start Production',
    action_name='third_step',
    description='Mark the start of production (no parameters required).',
    serializer_class=ThirdStepSwaggerSerializer,
    res={'200': steps_data[3]['status']},
)
action_fourth_step_decorator = action_swagger_documentation(
    summaries='Step 4: Finish Production',
    action_name='fourth_step',
    description='Mark the end of production (no parameters required).',
    serializer_class=FourthStepSwaggerSerializer,
    res={'200': steps_data[4]['status']},
)
action_fifth_step_decorator = action_swagger_documentation(
    summaries='Step 5: Post-Production Details',
    action_name='fifth_step',
    description='Register empty weight, losses, fuel usage, and other production details.',
    serializer_class=FifthStepSwaggerSerializer,
    res={'200': steps_data[5]['status']},
)
action_sixth_step_decorator = action_swagger_documentation(
    summaries='Step 6: Exit from Slaughter',
    action_name='sixth_step',
    description='Mark the exit from slaughter (no parameters required).',
    serializer_class=SixthStepSwaggerSerializer,
    res={'200': steps_data[6]['status']},
)
action_seventh_step_decorator = action_swagger_documentation(
    summaries='Step 7: Final Product Slaughter Number',
    action_name='seventh_step',
    description='Register final product slaughter number.',
    serializer_class=SeventhStepSwaggerSerializer,
    res={'200': steps_data[7]['status']},
)

# ImportProductFromWareHouseAPIView decorators
bulk_post_request_from_warehouse_decorator = custom_swagger_generator(
    serializer_class=ImportProductFromWareHouseSerializerPOST, method='bulk_post', many=True
)
single_post_request_from_warehouse_decorator = custom_swagger_generator(
    serializer_class=ImportProductFromWareHouseSerializerPOST, method='single_post', many=False
)
bulk_patch_request_from_warehouse_decorator = custom_swagger_generator(
    serializer_class=ImportProductFromWareHouseSerializer, method='bulk_patch', many=True
)
single_patch_request_from_warehouse_decorator = custom_swagger_generator(
    serializer_class=ImportProductFromWareHouseSerializer, method='single_patch', many=False
)
bulk_get_from_warehouse_decorator = custom_swagger_generator(
    serializer_class=ImportProductFromWareHouseSerializer, method='bulk_get', many=True
)
single_get_from_warehouse_decorator = custom_swagger_generator(
    serializer_class=ImportProductFromWareHouseSerializer, method='single_get', many=False
)
bulk_delete_request_from_warehouse_decorator = custom_swagger_generator(
    serializer_class=ImportProductFromWareHouseSerializer, method='bulk_delete', many=True
)
single_delete_request_from_warehouse_decorator = custom_swagger_generator(
    serializer_class=ImportProductFromWareHouseSerializer, method='single_delete', many=False
)
action_planned_from_warehouse_decorator = action_swagger_documentation(
    summaries='Plan the Import Product From Warehouse',
    action_name='planned',
    description='Plan the import product From Warehouse by updating the status to "planned".',
    serializer_class=IsStatusSwaggerSerializer,
    res={'200': is_status_dict['is_planned']},
)
action_cancel_from_warehouse_decorator = action_swagger_documentation(
    summaries='Cancel the Import Product From Warehouse',
    action_name='cancel',
    description='Cancel the import product From Warehouse by updating the status to "cancelled".',
    serializer_class=IsStatusSwaggerSerializer,
    res={'200': is_status_dict['is_cancelled']},
)
action_verify_from_warehouse_decorator = action_swagger_documentation(
    summaries='Verify the Import Product From Warehouse',
    action_name='verify',
    description='Verify the import product From Warehouse by updating the status to "verified".',
    serializer_class=IsStatusSwaggerSerializer,
    res={'200': is_status_dict['is_verified']},
)
action_start_from_warehouse_decorator = action_swagger_documentation(
    summaries='start production for Import Product From Warehouse',
    action_name='start',
    description='start production and register time and user',
    serializer_class=StartFinishImportProductFromWareHouseSwaggerSerializer,
    res={'200': warehouse_finish_start_200_status['production_start_date']},
)
action_finish_from_warehouse_decorator = action_swagger_documentation(
    summaries='finish production for Import Product From Warehouse',
    action_name='finish',
    description='finish production and register time and user',
    serializer_class=StartFinishImportProductFromWareHouseSwaggerSerializer,
    res={'200': warehouse_finish_start_200_status['production_finished_date']},
)
