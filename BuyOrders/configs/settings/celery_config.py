# configs/celery.py
import os
from celery import Celery
from django.conf import settings

DJANGO_SETTINGS_MODULE = os.getenv("DJANGO_SETTINGS_MODULE")
if not DJANGO_SETTINGS_MODULE:
    ENV = os.getenv("ENVIRONMENT", "development").lower()
    DJANGO_SETTINGS_MODULE = "configs.settings.deploy_settings" if ENV == "deployment" else "configs.settings.env_settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

app = Celery("BuyOrders")
broker_url = os.getenv("CELERY_BROKER_URL", getattr(settings, "CELERY_BROKER_URL", "amqp://localhost"))
app.conf.broker_url = broker_url
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
