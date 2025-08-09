import re
from typing import Dict, Any

import requests
import yaml

from utils.api_unittest import EndpointUnitTest
from utils.drf_schema import ExtractDRFSwaggerAPISchema


class DRFAPIUnitTesting(ExtractDRFSwaggerAPISchema):

    def __init__(self, swagger_api_schema_url: str, token: Dict = None, have_used_http_only_cookie: bool = True,
                 ip_server: str = 'http://127.0.0.1:8001/api/v1'):

        super().__init__(swagger_api_schema_url)

        self.token = token if token else {}
        self.have_used_http_only_cookie = have_used_http_only_cookie
        self.ip_server = ip_server

    def run_test(self) -> Dict:
        """
        run test on drf-swagger s api list with drf api schema and monitor apis test

        Returns:
            Dict[Any]: return api test's checking status

        """

        endpoint_data = self.extract_api_schema()
        api_test_report_data = {}

        for cnt, (endpoint, endpoint_schema) in enumerate(endpoint_data.items()):

            if self.token:
                endpoint_schema['token'] = self.token
                endpoint_schema['http_only_cookie'] = self.have_used_http_only_cookie
            endpoint_unittest_obj = EndpointUnitTest(**endpoint_schema)
            endpoint_unittest_obj.run_test()

        return api_test_report_data
