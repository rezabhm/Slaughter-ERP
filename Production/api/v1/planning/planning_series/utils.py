from django.http import JsonResponse
from rest_framework import status

from api.v1.planning.planning_series.conf import status_dict
from apps.planning.documents import PlanningSeries
from utils.models_utils import get_model_object


def handle_finished(user, slug_id, lookup_field, model=PlanningSeries):
    obj = get_model_object(model, {lookup_field: slug_id})

    if obj:
        if obj.is_finished:
            return JsonResponse(
                data={'message': f'Planning series with slug id {slug_id} is already finished'},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.is_finished = True
        obj.save()
        return JsonResponse(data=status_dict['finished'], status=status.HTTP_200_OK)

    return JsonResponse(
        data={'message': f'Object with slug id {slug_id} not found'},
        status=status.HTTP_404_NOT_FOUND
    )