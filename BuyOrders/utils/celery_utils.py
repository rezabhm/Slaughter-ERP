import time

import requests
from celery import shared_task


@shared_task
def store_logs_in_background(logs_data: dict, log_server_information: dict, token:str):

    """
    send logs_data to logging server

    Args:
        logs_data: logs data
        log_server_information: logs server information
        token: authentication token
    """

    _ = requests.post(url=log_server_information['endpoint_url'], json=logs_data,
                        headers={'Authorization': f'Bearer {token}'})
