from api.v1.order.invoice.conf import status_dict
from api.v1.order.invoice.swagger import AddPurchaseOrdersSwaggerSerializer
from apps.orders.serializers import InvoiceSerializer, InvoiceSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(serializer_class=InvoiceSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=InvoiceSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=InvoiceSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=InvoiceSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=InvoiceSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=InvoiceSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=InvoiceSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=InvoiceSerializer, method='single_delete', many=False)
action_add_purchase_orders_decorator = action_swagger_documentation(
    summaries='Add Purchase Orders to Invoice',
    action_name='add_purchase_orders',
    description='Add a list of PurchaseOrder IDs to the invoice product_list, setting have_factor=True in each PurchaseOrder. Returns error if any ID is invalid or already exists in the list.',
    serializer_class=AddPurchaseOrdersSwaggerSerializer,
    res={'200': status_dict['add_purchase_orders']}
)