from django.http import JsonResponse
from rest_framework import status

from api.v1.warehouse.transaction.conf import *
from apps.core.documents import CheckStatus, DateUser
from apps.warehouse.documents import Transaction
from utils.models_utils import get_model_object


def verify_transaction(user, slug, lookup_field):

    obj = get_model_object(Transaction, {lookup_field:slug})

    if obj:

        warehouse = obj.inventory.warehouse

        if warehouse.is_active:

            obj.is_verified = CheckStatus(status=True, user_date=DateUser(user=user))

            obj.save()

            return JsonResponse(data=http_200_transaction, status=status.HTTP_200_OK)

        else:
            obj.is_verified = CheckStatus(status=False, user_date=DateUser(user=user))
            obj.description = (f'you cant verify this transaction because ware house is not active right now.'
                               f' (date : {timezone.now()})')

            obj.save()

            return JsonResponse(data=http_400_transaction, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse(data=http_404_transaction, status=status.HTTP_404_NOT_FOUND)
