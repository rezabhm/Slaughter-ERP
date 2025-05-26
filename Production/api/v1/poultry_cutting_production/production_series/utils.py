from django.http import JsonResponse
from rest_framework import status

from api.v1.poultry_cutting_production.production_series.conf import start_finish_status
from apps.core.documents import DateUser
from apps.poultry_cutting_production.documents import PoultryCuttingProductionSeries
from utils.models_utils import get_model_object


def handle_start_finish(user, slug_id, lookup_field, action_type):
    obj = get_model_object(PoultryCuttingProductionSeries, {lookup_field: slug_id})

    if obj:
        if action_type == 'start' and obj.status == 'pending':
            obj.start = DateUser(user=user)
            obj.status = 'started'
        elif action_type == 'finish' and obj.status == 'started':
            obj.finished = DateUser(user=user)
            obj.status = 'finished'
        else:
            return JsonResponse(
                data={'message': f'Invalid action: cannot {action_type} from current status {obj.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.save()
        return JsonResponse(data=start_finish_status[action_type], status=status.HTTP_200_OK)

    return JsonResponse(
        data={'message': f'Object with slug id {slug_id} not found'},
        status=status.HTTP_404_NOT_FOUND
    )