from django.http import JsonResponse
from rest_framework import status

from api.v1.production.export_product.conf import *
from apps.core.documents import CheckStatus, DateUser
from apps.production.documents import ExportProduct
from utils.models_utils import get_model_object


def handle_status(user, slug, lookup_field):

    obj = get_model_object(ExportProduct, {lookup_field: slug})

    if obj:

        obj.is_verified_by_receiver_delivery_unit_user = CheckStatus(

            status=True,
            user_date=DateUser(user=user)
        )

        obj.save()

        return JsonResponse(data=status_200, status=status.HTTP_200_OK)

    return JsonResponse(data=status_404, status=status.HTTP_404_NOT_FOUND)
