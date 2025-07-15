from api.v1.order.purchase_order.conf import status_dict
from api.v1.order.purchase_order.swagger import *
from apps.orders.serializers import PurchaseOrderSerializer, PurchaseOrderSerializerPOST
from utils.swagger_utils.custom_swagger_generator import action_swagger_documentation, custom_swagger_generator

bulk_post_request_decorator = custom_swagger_generator(serializer_class=PurchaseOrderSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=PurchaseOrderSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='single_delete', many=False)
action_verified_finance_decorator = action_swagger_documentation(
    summaries='Verify Purchase Order by Finance',
    action_name='verified_finance',
    description='Verify the purchase order by finance department, updating approved_by_finance and status to "pending for approved by purchaser" or "rejected by financial".',
    serializer_class=VerifiedFinanceSwaggerSerializer,
    res={'200': status_dict['approved_by_finance']}
)
action_approved_by_purchaser_decorator = action_swagger_documentation(
    summaries='Approve Purchase Order by Purchaser',
    action_name='approved_by_purchaser',
    description='Approve the purchase order by purchaser, updating approved_by_purchaser, estimated_price, planned_purchase_date, and status to "pending for purchased" or "rejected by purchaser".',
    serializer_class=ApprovedByPurchaserSwaggerSerializer,
    res={'200': status_dict['approved_by_purchaser']}
)
action_purchased_decorator = action_swagger_documentation(
    summaries='Mark Purchase Order as Purchased',
    action_name='purchased',
    description='Mark the purchase order as purchased, updating purchased, final_price, and status to "pending for received" or "purchased failed".',
    serializer_class=PurchasedSwaggerSerializer,
    res={'200': status_dict['purchased']}
)
action_received_decorator = action_swagger_documentation(
    summaries='Mark Purchase Order as Received',
    action_name='received',
    description='Mark the purchase order as received, updating received, have_factor, and status to "add to factor" or "received failed".',
    serializer_class=ReceivedSwaggerSerializer,
    res={'200': status_dict['received']}
)
action_done_decorator = action_swagger_documentation(
    summaries='Mark Purchase Order as Done',
    action_name='done',
    description='Mark the purchase order as done, updating the status to "done".',
    serializer_class=DoneSwaggerSerializer,
    res={'200': status_dict['done']}
)
action_cancelled_decorator = action_swagger_documentation(
    summaries='Cancel Purchase Order',
    action_name='cancelled',
    description='Cancel the purchase order by updating the status to "cancelled".',
    serializer_class=CancelledSwaggerSerializer,
    res={'200': status_dict['cancelled']}
)