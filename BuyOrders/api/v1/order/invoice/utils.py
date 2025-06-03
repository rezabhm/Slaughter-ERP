from django.http import JsonResponse
from rest_framework import status
from api.v1.order.invoice.conf import http_200, http_404
from apps.orders.documents import Invoice, PurchaseOrder
from utils.models_utils import get_model_object

is_status_dict = {
    'add_purchase_orders': http_200
}


def set_status_400_status(slug_id):
    return http_404


def set_purchase_order_404_status(purchase_order_id):
    return {'message': f'PurchaseOrder with ID {purchase_order_id} does not exist'}


def set_purchase_order_exists_status(purchase_order_id):
    return {'message': f'PurchaseOrder with ID {purchase_order_id} already exists in the invoice product_list'}


def handle_add_purchase_orders(user, slug_id, lookup_field, validated_data, model=Invoice):
    obj = get_model_object(model, {lookup_field: slug_id})
    if not obj:
        return JsonResponse(data=set_status_400_status(slug_id), status=status.HTTP_404_NOT_FOUND)

    purchase_order_ids = validated_data.get('purchase_order', [])
    if not purchase_order_ids:
        return JsonResponse(data={'message': 'No PurchaseOrder IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Get current product_list IDs
    current_product_list = [str(po.id) for po in obj.product_list]

    for po_id in purchase_order_ids:
        # Check if PurchaseOrder exists
        po_obj = get_model_object(PurchaseOrder, {'id': po_id})
        if not po_obj:
            return JsonResponse(data=set_purchase_order_404_status(po_id), status=status.HTTP_404_NOT_FOUND)

        # Check if PurchaseOrder is already in product_list
        if str(po_id) in current_product_list:
            return JsonResponse(data=set_purchase_order_exists_status(po_id), status=status.HTTP_400_BAD_REQUEST)

    # Add valid PurchaseOrder IDs to product_list and update have_factor
    for po_id in purchase_order_ids:
        po_obj = get_model_object(PurchaseOrder, {'id': po_id})
        obj.product_list.append(po_obj)
        po_obj.have_factor = True
        po_obj.save()

    obj.save()
    return JsonResponse(data=is_status_dict['add_purchase_orders'], status=status.HTTP_200_OK)