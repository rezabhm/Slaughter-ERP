import json

from utils.api_unittest import EndpointUnitTest


class ManualEndpointUnitTesting:
    """

    json format example :

    {
      "ip_server": "",
      "token": {
        "access_token": "",
        "cookies_token_keyname": ""

      },
      "http_only_cookie": true,
      "apis": [

        {
          "endpoint": "",
          "data": {},
          "expected_response": {
            "body": {},
            "status_code": 200,
            "compare_format": ""
          }
        }

      ]

    }

    """


    json_data: dict = None

    def __init__(self, endpoint_json_path: str):

        self.load_json(json_path=endpoint_json_path)
        self.validation_status = self.is_valid()

    def load_json(self, json_path: str):
        """
        load endpoints json

        Args:
            json_path: path to endpoints json

        """
        with open(json_path, 'rb') as fd:
            self.json_data = json.load(fd)
            fd.close()

    def is_valid(self) -> bool:
        """
        check json data is valid or not, json data must have blew structure:
            {
                ipserver: '127.0.0.1:8000/api/v1/',
                token: {

                    access_token: 'dsdfsdfsdf.dsfsdf.dsfsdfsdf'
                    cookies_token_keyname : 'access_token'

                },
                http_only_cookie: True,

                apis: [

                    {
                        endpoint: 'buy/buy-user/'
                        data: {...params},
                        expected_response: {

                            body: {...params},
                            status_code: 200,
                            compare_format: equal/format_checking
                        },
                        method: 'GET'

                    },
                    ...
                ]
            }

        Returns:
            bool: return json validation status that determine json is valid or not
        """

        configs = {

            'ip_server': str,
            'token': dict,
            'http_only_cookie': bool,
            'apis': list

        }
        api_schema_configs = {

            'data': dict,
            'endpoint': str,
            'expected_response': dict,
            'method': str

        }

        expected_response_configs = {
            'body': dict,
            'status_code': int
        }

        if not isinstance(self.json_data, dict):
            raise KeyError('your json data must be dict type ')

        self.is_valid_dict(configs=configs, json_data=self.json_data)

        access_token = self.json_data['token'].get('access_token', None)
        if access_token is None:
            raise KeyError('your token object must include <access_token> key')

        for api in self.json_data['apis']:
            self.is_valid_dict(configs=api_schema_configs, json_data=api)
            self.is_valid_dict(configs=expected_response_configs, json_data=api['expected_response'])

            if 'compare_format' in api.keys() and api['compare_format'] not in ['equal', 'format_checking']:
                raise ValueError("your <compare_format> value must be one of this list"
                                 " item : ['equal', 'format_checking']")

        return True

    @staticmethod
    def is_valid_dict(configs: dict, json_data: dict):
        """
        check given dict is valid or not

        Args:
            configs: main dict that must match with it
            json_data: json data that we check

        """
        for key, key_type in configs.items():
            if key not in json_data.keys():
                raise KeyError(f'{key} not found in your json key list : [{configs.keys()}] ')

            if not isinstance(json_data[key], key_type):
                raise KeyError(f'yor key [{key}] must be <{key_type}> but got {type(json_data[key])}')

    def run_test(self):
        """
        run manual unit-test
        """

        ip_server = self.json_data['ip_server']
        token = self.json_data['token']
        http_only_cookie = self.json_data['http_only_cookie']

        for api in self.json_data['apis']:

            schema = api.copy()

            schema['endpoint'] = f'{ip_server}{api['endpoint']}'
            schema['token'] = token
            schema['http_only_cookie'] = http_only_cookie

            endpoint_testing_obj = EndpointUnitTest(**schema)
            endpoint_testing_obj.run_test()
