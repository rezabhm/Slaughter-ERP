from django.http import JsonResponse
from rest_framework import status

from api.v1.warehouse.warehouse.conf import *
from apps.warehouse.documents import Warehouse
from utils.models_utils import get_model_object


def handle_activation_status(slug, lookup_field):

    obj = get_model_object(Warehouse, {lookup_field:slug})

    if obj:

        obj.is_active = not obj.is_active
        obj.save()

        return JsonResponse(data=http_200, status=status.HTTP_200_OK)

    return JsonResponse(data=http_404, status=status.HTTP_404_NOT_FOUND)