from django.http import JsonResponse
from rest_framework import status
from api.v1.sale.truck_loading.conf import http_200, http_404, is_status_dict
from apps.core.documents import DateUser, CheckStatus
from apps.sale.documents import TruckLoading, CarWeight
from utils.models_utils import get_model_object

LEVEL_CHOICES = (
    ('entrance', 'entrance'),
    ('first_weighting', 'first_weighting'),
    ('last_weighting', 'last_weighting'),
    ('exit', 'exit'),
    ('cancel', 'cancel'),
)


def set_status_400_status(slug_id):
    return http_404


def set_car_weight_404_status(car_weight_id):
    return {'message': f'CarWeight with ID {car_weight_id} does not exist'}


def handle_first_weighting(user, slug, lookup_field, validated_data, model=TruckLoading):
    obj = get_model_object(model, {lookup_field: slug})
    if not obj:
        return JsonResponse(data=set_status_400_status(slug), status=status.HTTP_404_NOT_FOUND)

    car_weight = validated_data.get('first_weight')
    if not car_weight:
        return JsonResponse(data={'message': 'No CarWeight ID provided'}, status=status.HTTP_400_BAD_REQUEST)

    if obj.level not in ['entrance']:
        return JsonResponse(data={'message': f'Cannot set first_weighting, current level is {obj.level}'}, status=status.HTTP_400_BAD_REQUEST)

    obj.first_weight = CarWeight(weight=car_weight, date=DateUser(user=user))
    obj.level = 'first_weighting'
    obj.save()

    return JsonResponse(data=is_status_dict['first_weighting'], status=status.HTTP_200_OK)


def handle_last_weighting(user, slug, lookup_field, validated_data, model=TruckLoading):
    obj = get_model_object(model, {lookup_field: slug})
    if not obj:
        return JsonResponse(data=set_status_400_status(slug), status=status.HTTP_404_NOT_FOUND)

    car_weight = validated_data.get('last_weight')
    if not car_weight:
        return JsonResponse(data={'message': 'No CarWeight provided'}, status=status.HTTP_400_BAD_REQUEST)

    if obj.level not in ['first_weighting']:
        return JsonResponse(data={'message': f'Cannot set last_weighting, current level is {obj.level}'}, status=status.HTTP_400_BAD_REQUEST)

    obj.last_weight = CarWeight(weight=car_weight, date=DateUser(user=user))
    obj.level = 'last_weighting'
    obj.save()

    return JsonResponse(data=is_status_dict['last_weighting'], status=status.HTTP_200_OK)


def handle_exit(user, slug, lookup_field, validated_data, model=TruckLoading):
    obj = get_model_object(model, {lookup_field: slug})
    if not obj:
        return JsonResponse(data=set_status_400_status(slug), status=status.HTTP_404_NOT_FOUND)

    exit_date = validated_data.get('exit_date')
    if not exit_date:
        return JsonResponse(data={'message': 'No exit_date provided'}, status=status.HTTP_400_BAD_REQUEST)

    if obj.level not in ['last_weighting']:
        return JsonResponse(data={'message': f'Cannot set exit, current level is {obj.level}'}, status=status.HTTP_400_BAD_REQUEST)

    obj.exit_date = DateUser(user=user, date=exit_date)
    obj.level = 'exit'
    obj.save()

    return JsonResponse(data=is_status_dict['exit'], status=status.HTTP_200_OK)

def handle_cancel(user, slug, lookup_field, validated_data, model=TruckLoading):
    obj = get_model_object(model, {lookup_field: slug})
    if not obj:
        return JsonResponse(data=set_status_400_status(slug), status=status.HTTP_404_NOT_FOUND)

    if obj.level not in ['entrance', 'first_weighting', 'last_weighting']:
        return JsonResponse(data={'message': f'Cannot cancel, current level is {obj.level}'}, status=status.HTTP_400_BAD_REQUEST)

    obj.is_cancelled = CheckStatus(status=True, date=DateUser(user=user))
    obj.level = 'cancel'
    obj.save()

    return JsonResponse(data=is_status_dict['cancel'], status=status.HTTP_200_OK)