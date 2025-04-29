from django.core.exceptions import ObjectDoesNotExist

from apps.accounts.models import CustomUser


def get_user_by_id(user_id):
    try:
        return CustomUser.objects.get_by_natural_key(user_id)
    except ObjectDoesNotExist:
        return None
