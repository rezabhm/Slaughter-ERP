from apps.core.models import Core


def id_generator(class_name: str) -> str:
    """
    Generates a unique ID by incrementing the counter stored in the Core model.

    Args:
        class_name (str): The name used to identify the model class in the Core table.

    Returns:
        str: The new incremented ID as a string.
    """
    try:
        obj = Core.objects.get(name=class_name)
    except Core.DoesNotExist:
        obj = Core(name=class_name)
        obj.save()

    obj.increase()
    obj.save()

    return str(obj.value)
