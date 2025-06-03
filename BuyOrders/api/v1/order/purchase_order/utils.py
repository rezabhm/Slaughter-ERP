from django.http import JsonResponse
from rest_framework import status
from api.v1.order.purchase_order.conf import http_200, http_404
from apps.orders.documents import PurchaseOrder
from apps.core.documents import CheckStatus, DateUser
from utils.models_utils import get_model_object

is_status_dict = {
    'approved_by_finance': http_200,
    'approved_by_purchaser': http_200,
    'purchased': http_200,
    'received': http_200,
    'done': http_200,
    'cancelled': http_200
}

def set_status_400_status(slug_id):
    return http_404

def handle_status_action(user, slug_id, lookup_field, action_type, validated_data, model=PurchaseOrder):
    obj = get_model_object(model, {lookup_field: slug_id})
    if obj:
        action_status = validated_data.get('status', True)
        action_description = validated_data.get('description', '')

        # Set CheckStatus for the given action
        setattr(
            obj,
            action_type,
            CheckStatus(
                status=action_status,
                description=action_description,
                user_date=DateUser(user=user)
            )
        )

        # Update status based on action_type and validated_data['status']
        if action_type == 'approved_by_finance':
            obj.status = 'pending for approved by purchaser' if action_status else 'rejected by financial'

        elif action_type == 'approved_by_purchaser':
            obj.status = 'pending for purchased' if action_status else 'rejected by purchaser'
            if 'estimated_price' in validated_data:
                obj.estimated_price = validated_data['estimated_price']
            if 'planned_purchase_date' in validated_data:
                obj.planned_purchase_date = validated_data['planned_purchase_date']

        elif action_type == 'purchased':
            obj.status = 'pending for received' if action_status else 'purchased failed'
            if 'final_price' in validated_data:
                obj.final_price = validated_data['final_price']

        elif action_type == 'received':
            obj.status = 'add to factor' if action_status else 'received failed'
            if 'have_factor' in validated_data:
                obj.have_factor = validated_data['have_factor']

        elif action_type == 'done':
            obj.status = 'done'

        elif action_type == 'cancelled':
            obj.status = 'cancelled'

        obj.save()
        return JsonResponse(data=is_status_dict.get(action_type, http_200), status=status.HTTP_200_OK)

    return JsonResponse(data=set_status_400_status(slug_id), status=status.HTTP_404_NOT_FOUND)