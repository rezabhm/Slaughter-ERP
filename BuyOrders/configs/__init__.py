from django.conf import settings

if getattr(settings, 'CELERY_USE', False):

    from configs.settings.celery_config import app as celery_app

    __all__ = ("celery_app",)
