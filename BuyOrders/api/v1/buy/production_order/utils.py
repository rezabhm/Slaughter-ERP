from django.http import JsonResponse
from rest_framework import status
from api.v1.buy.production_order.conf import http_200, http_404
from apps.buy.documents import ProductionOrder
from apps.core.documents import CheckStatus, DateUser, Price
from utils.models_utils import get_model_object

is_status_dict = {
    'verified': http_200,
    'received': http_200,
    'finished': http_200,
    'done': http_200,
    'cancelled': http_200
}


def set_status_400_status(slug_id):
    return http_404


def handle_status(user, slug_id, lookup_field, action_type, validated_data, model=ProductionOrder):
    obj = get_model_object(model, {lookup_field: slug_id})
    if obj:
        action_status = validated_data.get('status', '')
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
        if action_type == 'done':
            obj.status = 'done'
            obj.weight = validated_data['weight']
            obj.quality = validated_data['quality']
            obj.price = Price(**validated_data['price'])

        elif action_type == 'cancelled':
            obj.status = 'cancelled'

        elif action_type == 'verified':
            obj.status = 'pending for received' if action_status else 'unverified'

        elif action_type == 'received':
            obj.status = 'pending for finished' if action_status else 'unreceived'

        elif action_type == 'finished':
            obj.status = 'pending for finished' if action_status else 'unfinished'

        obj.save()
        return JsonResponse(data=is_status_dict.get(action_type, http_200), status=status.HTTP_200_OK)

    return JsonResponse(data=set_status_400_status(slug_id), status=status.HTTP_404_NOT_FOUND)
