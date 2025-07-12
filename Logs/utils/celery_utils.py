import time

from celery import shared_task


@shared_task
def store_logs_in_background(logs_data: dict):

    """
    send logs_data to logging server

    Args:
        logs_data: logs data
    """
    print('running celery ')
