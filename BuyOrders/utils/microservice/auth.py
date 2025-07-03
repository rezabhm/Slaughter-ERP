import requests
from django.conf import settings


def load_slaughter_erp_token():

    with open('configs\\settings\\jwt\\token.txt', 'r') as fd:
        token = fd.read()
        fd.close()

    res = requests.get(settings.MICROSERVICE_URL['test_token'], headers={'Authorization': f'Bearer {token}'})

    if res.status_code in range(199, 299):
        return token
    else:

        username = settings.MICROSERVICE_CONFIGS['SlaughterERP']['username']
        password = settings.MICROSERVICE_CONFIGS['SlaughterERP']['password']

        post_request_data = {
            "username": username,
            "password": password
        }

        res = requests.post(settings.MICROSERVICE_URL['login'], json=post_request_data)

        if res.status_code in range(199, 299):
            with open('configs\\settings\\jwt\\token.txt', 'w') as fd:
                fd.write(res.json()['access'])
                fd.close()

            return res.json()['access']

        else:
            return None
