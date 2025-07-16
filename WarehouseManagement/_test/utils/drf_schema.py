import re
from typing import Any

import requests
import yaml


class ExtractDRFSwaggerAPISchema:

    def __init__(self, swagger_api_schema_url: str,):
        self.swagger_api_schema_url = swagger_api_schema_url
        self.api_schema = self.get_api_schema()

    def extract_api_schema(self) -> dict:

        """
        parser request's response from drf-swagger and extract schema

        Returns:
            Dict: return endpoints schema
        """

        endpoint_data = {}
        paths = self.api_schema.get('paths', {})

        for endpoint, endpoint_schema in paths.items():

            endpoint = self.correct_endpoint_url(endpoint)

            for endpoint_method, method_schema in endpoint_schema.items():

                # pass if method didn't http method
                if endpoint_method not in ['get', 'post', 'patch', 'put', 'delete']:
                    continue

                # get expected apis response schema
                request_response_schema = self.extract_response_schema(method_schema)

                # get requests body schema
                request_body_schema = self.extract_body_schema(method_schema)

                endpoint_data[f'{endpoint}@{endpoint_method}'] = {
                    'endpoint': endpoint,
                    'method': endpoint_method.upper(),
                    'data': request_body_schema,
                    'expected_response': {
                        'status_code': 200,
                        'body': request_response_schema
                    },
                }

        return endpoint_data

    def get_api_schema(self) -> dict[str, Any]:
        """
        request to server and get all api that register in drf swagger with apis schema and information

        Returns:
            Dict[str , Any]: return all apis schema in json format

        """

        try:
            print(self.swagger_api_schema_url)
            res = requests.get(self.swagger_api_schema_url)
        except Exception as e:
            print(f'cant send request to server {self.swagger_api_schema_url} \n Error -> {e}')
            return {}

        else:
            if res.status_code in range(199, 299):
                # load data from server and convert yaml data to json format
                return yaml.safe_load(res.text)
            else:
                raise ValueError(f'we cant get data from {self.swagger_api_schema_url}')

    def correct_endpoint_url(self, url: str) -> str:
        """
        add ipserver to endpoint url and fill in-path parameter

        Returns:
            str: return corrected endpoint url
        """

        url = f'{self.ip_server}{url}' if 'http' not in url else url

        slug_fields = re.findall(r'[{][\w]+[}]', url)
        for slug in slug_fields:
            url = url.replace(slug, 'test_id')

        return url

    @staticmethod
    def extract_response_schema(schema: dict) -> dict:

        """
        extract response schema from drf-swagger apis schema for unit-testing expected response

        Returns:
            Dict[Any] : return expected response for api
        """

        responses = schema.get('responses', {})

        # get raw response json
        response = {
            key: value['examples']['application/json']
            for key, value in responses.items() if int(key) in list(range(199, 299))
        }
        # get only firsts schema
        (_, response_schema) = response.popitem() if len(response.keys()) > 0 else (None, {})

        # split only 200 response
        for key, value in response_schema.items():
            if key in ['200', '201', '202', '203', '204']:
                response_schema = value

        return response_schema

    def extract_body_schema(self, schema: dict) -> dict:
        """
        extract apis requests schema from drf-swagger schema for unit-testing

        Returns:
            Dict : extract requests body schema

        """
        parameters = schema.get('parameters', [])
        parameters = parameters[0] if len(parameters) > 0 else {}

        if parameters.get('in', 'query') == 'body':
            request_schema = parameters['schema']['properties']
        else:
            request_schema = {}

        request_schema = self.generate_sample_data(request_schema)

        return request_schema

    def generate_sample_data(self, schema: dict[str, Any]) -> dict[str, Any]:
        """
        Generate a sample dictionary from a JSON schema with default values.

        Args:
            schema (Dict[str, Any]): JSON schema describing the data structure.

        Returns:
            Dict[str, Any]: Sample dictionary with default values based on the schema.
        """

        for key, value in schema.items():

            if 'id' == key:
                schema[key] = 'test_id'
                continue

            if key == 'required':
                continue

            type__ = value.get('type', None)
            default = value.get('default', None)

            if default:
                schema[key] = default
                continue

            if type__ == 'number':
                schema[key] = 1.0
            elif type__ == 'integer':
                schema[key] = 1
            elif type__ == 'string':
                schema[key] = 'test_str'
            elif type__ == 'boolean':
                schema[key] = True
            elif type__ == 'object':
                schema[key] = self.generate_sample_data(value['properties'])
            elif type__ == 'array':
                item = {'properties': value['items']}
                schema[key] = [self.generate_sample_data(item)['properties']]
            else:
                schema[key] = None

        return schema
