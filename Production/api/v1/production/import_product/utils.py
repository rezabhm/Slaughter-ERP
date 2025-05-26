from django.http import JsonResponse
from rest_framework import status

from api.v1.production.import_product.conf import *
from apps.core.documents import CheckStatus, DateUser
from apps.production.documents import ImportProduct, ImportProductFromWareHouse
from utils.models_utils import get_model_object


def handle_status(user, slug_id, lookup_field, action_type, model=ImportProduct):

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

        return JsonResponse(data=is_status_dict[action_type], status=status.HTTP_200_OK)

    return JsonResponse(data=set_status_400_status(slug_id), status=status.HTTP_404_NOT_FOUND)


def build_embedded_model(step_data, data, username):

    model_instance = step_data['model']()

    for param in step_data['data']['user_date']:
        setattr(model_instance, param, DateUser(user=username))

    for param in step_data['data']['param']:
        setattr(model_instance, param, data[param])

    return model_instance


def handle_steps(request, slug, lookup_field, step=1):

    obj = get_model_object(ImportProduct, {lookup_field: slug})
    data = request.data

    if obj:

        object_step_data = steps_data[step]

        embedded_model = build_embedded_model(
            step_data=object_step_data,
            data=data,
            username=request.user_payload['username']
        )

        setattr(

            obj,
            object_step_data['model_attribute'],
            embedded_model

        )

        obj.level += 1

        obj.save()

        return JsonResponse(data=object_step_data['status'], status=status.HTTP_200_OK)

    return JsonResponse(data=steps_400_status, status=status.HTTP_400_BAD_REQUEST)


def handle_start_finish(user, slug_id, lookup_field, action_type):

    obj = get_model_object(ImportProductFromWareHouse, {lookup_field: slug_id})

    if obj:

        setattr(obj, action_type, DateUser(
            user=user
        ))

        obj.save()

        return JsonResponse(data=warehouse_finish_start_200_status['status'], status=status.HTTP_200_OK)

    return JsonResponse(data=set_status_400_status(slug_id), status=status.HTTP_404_NOT_FOUND)