from django.http import JsonResponse
from rest_framework import status

from api.v1.production.return_product.conf import *
from apps.core.documents import CheckStatus, DateUser
from apps.production.documents import ReturnProduct
from utils.models_utils import get_model_object


def handle_verify(request, slug, lookup_field):

    obj = get_model_object(ReturnProduct, {lookup_field:slug})
    data = request.data

    if obj:

        obj.verified = CheckStatus(
            status=False,
            user_date=DateUser(user=request.user_payload['username'])
        )

        obj.is_useful = data['is_useful']
        obj.is_repack = data['is_repack']

        obj.save()

        return JsonResponse(data=status_200, status=status.HTTP_200_OK)

    return JsonResponse(data=status_404, status=status.HTTP_404_NOT_FOUND)