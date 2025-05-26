from django.http import JsonResponse
from rest_framework import status

from api.v1.poultry_cutting_production.export_product.conf import status_dict
from apps.core.documents import CheckStatus, DateUser
from apps.poultry_cutting_production.documents import PoultryCuttingExportProduct
from utils.models_utils import get_model_object

def handle_status(user, slug_id, lookup_field, action_type, model=PoultryCuttingExportProduct):
    obj = get_model_object(model, {lookup_field: slug_id})

    if obj:
        setattr(
            obj,
            action_type,
            CheckStatus(
                status=True,
                user_date=DateUser(user=user)
            )
        )

        obj.save()
        return JsonResponse(data=status_dict[action_type], status=status.HTTP_200_OK)

    return JsonResponse(
        data={'message': f'Object with slug id {slug_id} not found'},
        status=status.HTTP_404_NOT_FOUND
    )