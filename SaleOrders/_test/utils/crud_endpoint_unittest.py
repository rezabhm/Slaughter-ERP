import pprint
import random
import time
from datetime import timezone
from typing import Any

import requests

from utils._requests import CustomRequest
from utils.api_unittest import EndpointUnitTest
from utils.drf_schema import ExtractDRFSwaggerAPISchema


def get_crud_urls(endpoint: str) -> list[dict]:
    """
    return GET,PATCH,POST,DELETE url for crud operation

    Args:
        endpoint: endpoints base url

    Returns:
        list[dict] = list of crud operation with its priority to send reqeust and methods

    """

    return [

        # single operation
        {
            'url': f'{endpoint}c/',
            'method': 'POST',
            'title': 'single post request'
        },
        {
            'url': f'{endpoint}s/<id>/',
            'method': 'GET',
            'title': 'single get request'
        },
        {
            'url': f'{endpoint}s/<id>/',
            'method': 'PATCH',
            'title': 'single patch request'
        },
        {
            'url': f'{endpoint}s/<id>/',
            'method': 'GET',
            'title': 'single get request'
        },
        {
            'url': f'{endpoint}s/<id>/',
            'method': 'DELETE',
            'title': 'single delete request'
        },
        {
            'url': f'{endpoint}s/<id>/',
            'method': 'GET',
            'title': 'single get request'
        },

        # bulk operation
        {
            'url': endpoint,
            'method': 'POST',
            'title': 'bulk post request'
        },
        {
            'url': endpoint,
            'method': 'GET',
            'title': 'bulk get request'
        },
        {
            'url': endpoint,
            'method': 'PATCH',
            'title': 'bulk patch request'
        },
        {
            'url': endpoint,
            'method': 'GET',
            'title': 'bulk get request'
        },
        {
            'url': endpoint,
            'method': 'DELETE',
            'title': 'bulk delete request'
        },
        {
            'url': endpoint,
            'method': 'GET',
            'title': 'bulk get request'
        },

    ]


class EndpointCRUDUnitTesting(ExtractDRFSwaggerAPISchema, CustomRequest):
    map_method_to_request = {

        'POST': requests.post,
        'GET': requests.get,
        'PATCH': requests.patch,
        'DELETE': requests.delete

    }

    def __init__(self, swagger_api_schema_url: str, ip_server: str, endpoints: list[str], token: dict = None,
                 have_used_http_only_cookie: bool = False):

        ExtractDRFSwaggerAPISchema.__init__(self, swagger_api_schema_url=swagger_api_schema_url)
        CustomRequest.__init__(self)

        self.ip_server = ip_server
        self.endpoints = endpoints
        self.token = token if token else {}
        self.have_used_http_only_cookie = have_used_http_only_cookie

    def run_test(self) -> dict:
        """
        run test for testing crud

        Returns:
            dict: return Testing result for endpoints

        """

        """
        example schema
        apis_schema = [

             'http://127.0.0.1:8001/api/v1/order/purchase-order/test_id/verified_finance/@post': {

                    'data': {'status': 'pending '
                                         'for '
                                         'approved '
                                         'by '
                                         'financial '
                                         'department'},

                    'endpoint': 'http://127.0.0.1:8001/api/v1/order/purchase-order/test_id/verified_finance/',

                    'expected_response': {

                            'body': {
                                        'message': 'Purchase order successfully verified by finance'
                                    },
                            'status_code': 200
                                    },

                    'method': 'POST'

                    }

        ]
        """

        apis_schema = self.extract_api_schema()

        for endpoint in self.endpoints:

            get_cruds_urls = get_crud_urls(f'{self.ip_server}{endpoint}')
            pre_response = requests.Response

            for idx, url_inf in enumerate(get_cruds_urls):

                schema_url_key = f'{url_inf['url'].replace('<id>', 'test_id')}@{url_inf['method'].lower()}'
                api_schema = apis_schema.get(schema_url_key, {})

                if self.token:
                    api_schema['token'] = self.token
                    api_schema['http_only_cookie'] = self.have_used_http_only_cookie

                test_result, pre_response = self.test_endpoint(schema=api_schema, idx=idx, pre_response=pre_response)

                if pre_response is None:
                    break

                if idx == 11:
                    break

    def test_endpoint(self, schema: dict, idx: int, pre_response: dict) -> [dict, dict]:

        """
        send request to endpoint and return result

        Args:
            schema: endpoint schema include endpoint data
            idx : idx of request priority
            pre_response : previous request's response

        Returns:
            response: requests response
        """

        if idx in [0, 6]:

            if idx == 6:
                schema['data']['data'] = [schema['data']['data'][0] for _ in range(2)]
                schema['expected_response']['body']['data'] = [schema['expected_response']['body']['data'][0] for _ in
                                                               range(2)]

            test_obj = EndpointUnitTest(**schema)
            test_result = test_obj.run_test()

            # print('\n\n\n')
            if test_result['is_success']:
                return test_result, test_result['response'].json()

            else:
                return test_result, None

        elif idx in [1, 3, 5]:

            if idx == 3:
                schema['expected_response']['body'] = pre_response
                schema['expected_response']['compare_format'] = 'equal'

            elif idx == 5:
                schema['expected_response']['status_code'] = 404
                schema['expected_response']['body'] = {
                    'message': 'object didnt find'
                }
                schema['expected_response']['compare_format'] = 'format_checking'

            schema['endpoint'] = schema['endpoint'].replace('test_id', pre_response['id'])
            test_obj = EndpointUnitTest(**schema)
            test_result = test_obj.run_test()

            if test_result['is_success']:
                return test_result, test_result['response'].json()

            else:
                return test_result, None

        elif idx in [2, 8]:

            if idx == 8:
                schema['data']['data'] = [
                    self.replace_data(schema['data']['data'][0].copy(), id_=pre_response['data'][i]['id']) for i in
                    range(2)]
                schema['expected_response']['body']['data'] = schema['data']['data']

                schema['expected_response']['compare_format'] = 'equal'

            else:

                schema['data'] = self.replace_data(data=schema['data'], id_=pre_response['id'])
                schema['endpoint'] = schema['endpoint'].replace('test_id', pre_response['id'])

            test_obj = EndpointUnitTest(**schema)
            test_result = test_obj.run_test()

            if test_result['is_success']:
                return test_result, schema['data']

            else:
                return test_result, None

        elif idx in [4, 10]:

            if idx == 10:
                schema['data']['data'] = [dt['id'] for dt in pre_response['data']]
                schema['expected_response']['body']['data'] = { id_: schema['expected_response']['body']['data']['test_str']
                for id_ in schema['data']['data'] }
                schema['expected_response']['compare_format'] = 'equal'

                # pprint.pprint(schema)
                # print('\n\n')
                # pprint.pprint(pre_response)
            else:
                schema['endpoint'] = schema['endpoint'].replace('test_id', pre_response['id'])

            test_obj = EndpointUnitTest(**schema)
            test_result = test_obj.run_test()
            if test_result['is_success']:
                return test_result, pre_response

            else:
                return test_result, None

        elif idx in [7, 9,11 ]:

            expected_id_list = [dt['id'] for dt in pre_response.get('data', []) if dt.get('id', None)]

            test_obj = EndpointUnitTest(**schema)
            test_result = test_obj.run_test()

            if test_result['is_success']:

                response_id_list = [dt['id'] for dt in test_result.get('response').json().get('data', []) if
                                    dt.get('id', None)]
                for id_ in expected_id_list:
                    if id_ not in response_id_list:
                        if idx in [11]:
                            print(f'{idx}) Error in {schema['method'].upper()}:{schema['endpoint']}')

                return test_result, {
                    'data': [dt for dt in test_result['response'].json()['data'] if dt['id'] in expected_id_list]}

            else:
                return test_result, None

        else:
            pass

    def replace_data(self, data: [dict, list], id_: str = 'test_id') -> [dict, list]:

        """
        replace data with new data

        Args:
            data: data for send reqeust
            id_: pre objects id

        Returns:
            dict: data that have changed data
        """

        if isinstance(data, dict):

            for key, value in data.items():

                if 'id' in key:
                    data[key] = id_
                    continue
                elif 'date' == key:
                    data[key] = time.ctime(time.time())
                    continue

                if isinstance(value, dict):
                    data[key] = self.replace_data(value)

                elif isinstance(value, list):
                    data[key] = self.replace_data(value)

                else:

                    data[key] = self.generate_new_data(value)

            return data

        elif isinstance(data, list):

            new_list = []

            for item in data:

                if isinstance(item, dict):
                    new_list.append(self.replace_data(item))

                elif isinstance(item, list):
                    new_list.append(self.replace_data(item))

                else:
                    new_list.append(self.generate_new_data(item))

            return new_list

        else:
            return data

    @staticmethod
    def generate_new_data(value: Any) -> Any:

        """
        regenerate new data

        Args:
            value: this is old value that we replacement with new data

        Returns:
            Any: generate new data
        """

        if isinstance(value, str) and value == 'test_str':
            return ''.join([random.choice(list('qwertyuiopasdfghjklzxcvbnm')) for _ in range(10)])

        elif type(value) is type(1):
            return random.choice(range(1, 1000000))

        elif type(value) is type(1.0):
            return float(random.choice(range(1, 10000000)))

        elif type(value) is type(True):
            return random.choice([True, False])
        else:
            return value
