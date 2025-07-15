from typing import Optional
import requests
from django.conf import settings


def load_slaughter_erp_token() -> Optional[str]:
    """
    Load or refresh the Slaughter ERP authentication token.

    Returns:
        Optional[str]: The valid JWT token if available, else None.
    """
    try:
        # Attempt to read existing token from file
        with open('configs/settings/jwt/token.txt', 'r') as fd:
            token = fd.read().strip()

        # Verify token validity
        response = requests.get(
            settings.MICROSERVICE_URL['test_token'],
            headers={'Authorization': f'Bearer {token}'}
        )

        if 199 <= response.status_code <= 299:
            return token

    except (FileNotFoundError, requests.RequestException):
        pass

    # Token invalid or not found, attempt to refresh
    try:
        auth_data = {
            'username': settings.MICROSERVICE_CONFIGS['SlaughterERP']['username'],
            'password': settings.MICROSERVICE_CONFIGS['SlaughterERP']['password']
        }

        response = requests.post(
            settings.MICROSERVICE_URL['login'],
            json=auth_data
        )

        if 199 <= response.status_code <= 299:
            new_token = response.json()['access']
            with open('configs/settings/jwt/token.txt', 'w') as fd:
                fd.write(new_token)
            return new_token

    except (requests.RequestException, KeyError, FileNotFoundError):
        pass

    return None