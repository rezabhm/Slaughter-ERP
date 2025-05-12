from apps.core.models import Core


def id_generator(class_name):

    try:
        obj = Core.objects.get(name=class_name)
    except:
        obj = Core(name='name')
        obj.save()

    obj.increase()
    obj.save()

    return str(obj.value)
