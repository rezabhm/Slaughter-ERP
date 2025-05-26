from django.http import JsonResponse
from rest_framework import status

from api.v1.production.production_series.conf import *
from apps.core.documents import DateUser


def production_series_change_status(request, slug_id, lookup_field, get_query, ps_status='start'):

    if slug_id:

        obj = get_query({lookup_field: slug_id})
        if isinstance(obj, JsonResponse) or not obj:
            return obj if obj else JsonResponse(data=start_finish_action_400(),
                                                status=status.HTTP_400_BAD_REQUEST)

        if ps_status == 'start':
            obj.start = DateUser(user=request.user_payload['username'])
            obj.status = 'started'

        else:
            obj.finish = DateUser(user=request.user_payload['username'])
            obj.status = 'finished'

        obj.save()

        return JsonResponse(data=start_finish_action_200(ps_status), status=status.HTTP_200_OK)

    return JsonResponse(data=start_finish_action_400(), status=status.HTTP_400_BAD_REQUEST)
