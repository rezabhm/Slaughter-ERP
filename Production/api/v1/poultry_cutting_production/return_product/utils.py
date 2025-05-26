from django.http import JsonResponse
from rest_framework import status

from api.v1.poultry_cutting_production.return_product.conf import status_dict
from apps.core.documents import DateUser, CheckStatus
from apps.poultry_cutting_production.documents import PoultryCuttingReturnProduct
from utils.models_utils import get_model_object


def handle_verify(user, slug_id, lookup_field, data, model=PoultryCuttingReturnProduct):
    obj = get_model_object(model, {lookup_field: slug_id})

    if obj:
        obj.verified = CheckStatus(
            status=True,
            user_date=DateUser(user=user)
        )
        obj.is_verified_by_receiver_delivery_unit_user = True

        # Update is_useful and is_repack from request.data if provided
        if 'is_useful' in data:
            obj.is_useful = data['is_useful']
        if 'is_repack' in data:
            obj.is_repack = data['is_repack']

        obj.save()
        return JsonResponse(data=status_dict['verified'], status=status.HTTP_200_OK)

    return JsonResponse(
        data={'message': f'Object with slug id {slug_id} not found'},
        status=status.HTTP_404_NOT_FOUND
    )