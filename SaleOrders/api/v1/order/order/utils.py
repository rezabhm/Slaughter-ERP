from django.http import JsonResponse
from rest_framework import status
from api.v1.order.order.conf import http_404, is_status_dict
from apps.core.documents import DateUser, CheckStatus, Car
from apps.order.documents import Order
from utils.models_utils import get_model_object


def set_status_400_status(slug_id):
    return http_404


def handle_attachment_status(user, slug, lookup_field, validated_data, model=Order):
    obj = get_model_object(model, {lookup_field: slug})
    if not obj:
        return JsonResponse(data=set_status_400_status(slug), status=status.HTTP_404_NOT_FOUND)

    car_id = validated_data.get('car')
    if not car_id:
        return JsonResponse(data={'message': 'car id didnt find in request data'}, status=status.HTTP_404_NOT_FOUND)

    car_obj = Car.objects(id=car_id).first

    obj.attachment_status = CheckStatus(status=True, date=DateUser(user=user))
    obj.car = car_obj

    obj.save()

    return JsonResponse(data=is_status_dict['attachment_status'], status=status.HTTP_200_OK)


def handle_verified(user, slug, lookup_field, validated_data, model=Order):
    obj = get_model_object(model, {lookup_field: slug})
    if not obj:
        return JsonResponse(data=set_status_400_status(slug), status=status.HTTP_404_NOT_FOUND)

    verified_status = validated_data.get('status')
    if not verified_status:
        return JsonResponse(data={'message': 'status didnt find in request data'}, status=status.HTTP_404_NOT_FOUND)

    obj.verified = CheckStatus(status=verified_status, date=DateUser(user=user))
    obj.save()

    return JsonResponse(data=is_status_dict['verified'], status=status.HTTP_200_OK)


def handle_cancelled(user, slug, lookup_field, validated_data, model=Order):
    obj = get_model_object(model, {lookup_field: slug})
    if not obj:
        return JsonResponse(data=set_status_400_status(slug), status=status.HTTP_404_NOT_FOUND)

    obj.cancelled = CheckStatus(status=True, date=DateUser(user=user))
    obj.save()

    return JsonResponse(data=is_status_dict['cancelled'], status=status.HTTP_200_OK)