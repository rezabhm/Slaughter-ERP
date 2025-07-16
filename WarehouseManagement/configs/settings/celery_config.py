import os
from celery import Celery
from django.conf import settings

if getattr(settings, 'CELERY_USE', False):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings.dev')

    app = Celery("WarehouseManagement")

    # Read settings from settings.py
    app.config_from_object("django.conf:settings", namespace="CELERY")

    # Automatically discover tasks in applications
    app.autodiscover_tasks()

    @app.task(bind=True)
    def debug_task(self):
        print(f"Request: {self.request!r}")
