from django.utils.decorators import method_decorator

from api.v1.production.import_product.conf import *
from api.v1.production.import_product.swagger import *
from api.v1.production.import_product.utils import handle_steps, handle_status, \
    handle_start_finish
from apps.production.documents import ImportProduct, ImportProductFromWareHouse
from apps.production.serializers.import_product_serializer import ImportProductSerializer, ImportProductSerializerPOST, \
    ImportProductFromWareHouseSerializer, ImportProductFromWareHouseSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_delete', many=False))
@method_decorator(name='action_planned', decorator=action_swagger_documentation(summaries='Plan the Import Product', action_name='planned', description='Plan the import product by updating the status to "planned".', serializer_class=IsStatusSwaggerSerializer, res={'200': is_status_dict['is_planned']}))
@method_decorator(name='action_cancel', decorator=action_swagger_documentation(summaries='Cancel the Import Product', action_name='cancel', description='Cancel the import product by updating the status to "cancelled".', serializer_class=IsStatusSwaggerSerializer, res={'200': is_status_dict['is_cancelled']}))
@method_decorator(name='action_verify', decorator=action_swagger_documentation(summaries='Verify the Import Product', action_name='verify', description='Verify the import product by updating the status to "verified".', serializer_class=IsStatusSwaggerSerializer, res={'200': is_status_dict['is_verified']}))
@method_decorator(name='action_first_step', decorator=action_swagger_documentation(summaries='Step 1: Entrance to Slaughter', action_name='first_step', description='Record entrance to slaughter time.', serializer_class=FirstStepSwaggerSerializer, res={'200': steps_data[1]['status']}))
@method_decorator(name='action_second_step', decorator=action_swagger_documentation(summaries='Step 2: Weight and Cage Details', action_name='second_step', description='Register full weight, source weight, cage number, and number of products per cage.', serializer_class=SecondStepSwaggerSerializer, res={'200': steps_data[2]['status']}))
@method_decorator(name='action_third_step', decorator=action_swagger_documentation(summaries='Step 3: Start Production', action_name='third_step', description='Mark the start of production (no parameters required).', serializer_class=ThirdStepSwaggerSerializer, res={'200': steps_data[3]['status']}))
@method_decorator(name='action_fourth_step', decorator=action_swagger_documentation(summaries='Step 4: Finish Production', action_name='fourth_step', description='Mark the end of production (no parameters required).', serializer_class=FourthStepSwaggerSerializer, res={'200': steps_data[4]['status']}))
@method_decorator(name='action_fifth_step', decorator=action_swagger_documentation(summaries='Step 5: Post-Production Details', action_name='fifth_step', description='Register empty weight, losses, fuel usage, and other production details.', serializer_class=FifthStepSwaggerSerializer, res={'200': steps_data[5]['status']}))
@method_decorator(name='action_sixth_step', decorator=action_swagger_documentation(summaries='Step 6: Exit from Slaughter', action_name='sixth_step', description='Mark the exit from slaughter (no parameters required).', serializer_class=SixthStepSwaggerSerializer, res={'200': steps_data[6]['status']}))
@method_decorator(name='action_seventh_step', decorator=action_swagger_documentation(summaries='Step 7: Final Product Slaughter Number', action_name='seventh_step', description='Register final product slaughter number.', serializer_class=SeventhStepSwaggerSerializer, res={'200': steps_data[7]['status']}))
class ImportProductByCarAPIView(CustomAPIView):

    model = ImportProduct
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {

        'GET': ImportProductSerializer,
        'POST': ImportProductSerializerPOST,
        'PATCH': ImportProductSerializer,
        'PERFORM_ACTION': {}

    }

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],

    }

    def get_queryset(self):
        return ImportProduct.objects()

    def action_planned(self, request, slug=None):

        return handle_status(

            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_planned'

        )

    def action_cancel(self, request, slug=None):

        return handle_status(

            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_cancelled'

        )

    def action_verify(self, request, slug=None):
        return handle_status(

            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_verified'

        )

    def action_first_step(self, request, slug=None):

        return handle_steps(
            request=request,
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            step=1

        )

    def action_second_step(self, request, slug=None):

        return handle_steps(
            request=request,
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            step=2

        )

    def action_third_step(self, request, slug=None):
        return handle_steps(
            request=request,
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            step=3

        )

    def action_fourth_step(self, request, slug=None):
        return handle_steps(
            request=request,
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            step=4

        )

    def action_fifth_step(self, request, slug=None):
        return handle_steps(
            request=request,
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            step=5

        )

    def action_sixth_step(self, request, slug=None):
        return handle_steps(
            request=request,
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            step=6

        )

    def action_seventh_step(self, request, slug=None):
        return handle_steps(
            request=request,
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            step=7

        )


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=ImportProductFromWareHouseSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=ImportProductFromWareHouseSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=ImportProductFromWareHouseSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=ImportProductFromWareHouseSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=ImportProductFromWareHouseSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=ImportProductFromWareHouseSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=ImportProductFromWareHouseSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=ImportProductFromWareHouseSerializer, method='single_delete', many=False))
@method_decorator(name='action_planned', decorator=action_swagger_documentation(summaries='Plan the Import Product From Warehouse', action_name='planned', description='Plan the import product From Warehouse by updating the status to "planned".', serializer_class=IsStatusSwaggerSerializer, res={'200': is_status_dict['is_planned']}))
@method_decorator(name='action_cancel', decorator=action_swagger_documentation(summaries='Cancel the Import Product From Warehouse', action_name='cancel', description='Cancel the import product From Warehouse by updating the status to "cancelled".', serializer_class=IsStatusSwaggerSerializer, res={'200': is_status_dict['is_cancelled']}))
@method_decorator(name='action_verify', decorator=action_swagger_documentation(summaries='Verify the Import Product From Warehouse', action_name='verify', description='Verify the import product From Warehouse by updating the status to "verified".', serializer_class=IsStatusSwaggerSerializer, res={'200': is_status_dict['is_verified']}))
@method_decorator(name='action_start', decorator=action_swagger_documentation(summaries='start production for Import Product From Warehouse', action_name='start', description='start production and register time and user', serializer_class=StartFinishImportProductFromWareHouseSwaggerSerializer, res={'200': warehouse_finish_start_200_status['production_start_date']}))
@method_decorator(name='action_finish', decorator=action_swagger_documentation(summaries='finish production for Import Product From Warehouse', action_name='finish', description='finish production and register time and user', serializer_class=StartFinishImportProductFromWareHouseSwaggerSerializer, res={'200': warehouse_finish_start_200_status['production_finished_date']}))
class ImportProductFromWareHouseAPIView(CustomAPIView):

    model = ImportProductFromWareHouse
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {

        'GET': ImportProductFromWareHouseSerializer,
        'POST': ImportProductFromWareHouseSerializerPOST,
        'PATCH': ImportProductFromWareHouseSerializer,
        'PERFORM_ACTION': {}

    }

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],

    }

    def get_queryset(self):
        return ImportProductFromWareHouse.objects()

    def action_planned(self, request, slug=None):
        return handle_status(

            model=ImportProductFromWareHouse,
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_planned'

        )

    def action_cancel(self, request, slug=None):

        return handle_status(

            model=ImportProductFromWareHouse,
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_cancelled'

        )

    def action_verify(self, request, slug=None):
        return handle_status(

            model=ImportProductFromWareHouse,
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_verified'

        )

    def action_start(self, request, slug=None):
        return handle_start_finish(

            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='production_start_date'

        )

    def action_finish(self, request, slug=None):
        return handle_start_finish(

            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='production_finished_date'

        )
