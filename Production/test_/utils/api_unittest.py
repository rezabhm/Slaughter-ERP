from typing import Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import logging
from colorlog import ColoredFormatter

from utils._requests import CustomRequest

# Configure logger with colored output
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s: %(message)s",
    log_colors={"INFO": "green", "ERROR": "red"}
)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.setLevel(logging.INFO)

class EndpointUnitTest(CustomRequest):
    """A class to test API endpoints with configurable HTTP requests and response validation.

    Attributes:
        endpoint (str): The API endpoint URL to test.
        method (str): HTTP method (GET, POST, etc.). Defaults to 'GET'.
        token (Optional[Dict[str, Any]]): Authentication token details. Defaults to None.
        http_only_cookie (bool): Whether to use HTTP-only cookies. Defaults to False.
        data (Dict[str, Any]): Request payload or query parameters. Defaults to empty dict.
        expected_response (Dict[str, Any]): Expected response details. Defaults to status 200 and empty body.

    Example:
        ```python
        tester = EndpointTester(
            endpoint="https://api.example.com/items/42",
            method="GET",
            token={"access_token": "abc123"},
            data={"include": "details"},
            expected_response={"status_code": 200, "body": {"id": 42, "name": "Test Item"}}
        )
        result = tester.run_test()
        print(result)
        ```
    """

    def __init__(self, endpoint: str, method: str = "GET", token: Optional[Dict[str, Any]] = None,
                 http_only_cookie: bool = False, data: Optional[Dict[str, Any]] = None,
                 expected_response: Optional[Dict[str, Any]] = None):
        """Initialize the EndpointTester with the provided configuration."""
        super().__init__()
        self.endpoint = endpoint
        self.method = method.upper()
        self.token = token
        self.http_only_cookie = http_only_cookie
        self.data = data or {}
        self.expected_response = expected_response or {"status_code": 200, "body": {}}
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """Validate input parameters to ensure they are correct."""
        if not self.endpoint:
            raise ValueError("Endpoint URL cannot be empty")
        if self.method not in self._METHOD_MAP:
            raise ValueError(f"Unsupported HTTP method: {self.method}")
        if self.token and "access_token" not in self.token:
            raise ValueError("Token must include 'access_token' key")

    def run_test(self) -> Dict[str, Any]:
        """Execute the API test and return the result.

        Returns:
            Dict[str, Any]: Test result containing success status, validation details, and report.
        """
        try:
            response = self._send_request()
            validation_result = self._validate_response(response)
            report = self._generate_report(validation_result)
            log_level = logging.INFO if validation_result["is_success"] else logging.ERROR
            logger.log(log_level, report)
            return {
                "is_success": validation_result["is_success"],
                "validation_result": validation_result,
                "report": report,
                'response': response
            }
        except RequestException as e:
            report = f"Test FAILED for {self.endpoint}: {str(e)}"
            logger.error(report)
            return {"is_success": False, "error": str(e), "report": report}

    def _validate_response(self, response: requests.Response) -> Dict[str, Any]:
        """Validate the API response against expected values.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            Dict[str, Any]: Validation result with status code and body validation details.
        """

        is_status_code_valid = response.status_code == self.expected_response.get("status_code", 200)
        try:
            response_body = response.json()
        except ValueError:
            response_body = response.text

        is_body_valid, validation_description = self._validate_response_data(
            response=response_body,
            expected_response=self.expected_response.get("body", {}),
            compare_format=self.expected_response.get("compare_format", "format_checking")
        )

        return {
            "is_success": is_status_code_valid and is_body_valid,
            "is_status_code_valid": is_status_code_valid,
            "is_body_valid": is_body_valid,
            "response_status_code": response.status_code,
            "expected_status_code": self.expected_response.get("status_code", 200),
            "response_body": response_body,
            "expected_body": self.expected_response.get("body", {}),
            "method": response.request.method,
            "validation_description": validation_description
        }

    def _validate_response_data(self, response: Any, expected_response: Dict,
                                compare_format: str = "format_checking") -> [bool, str]:
        """Validate response data against expected response.

        Args:
            response (Any): The actual response body (dict or str).
            expected_response (Dict): The expected response body.
            compare_format (str): Comparison mode ('equal' or 'format_checking').

        Returns:
            bool: True if the response matches the expected response, False otherwise.
            str: checking status description
        """

        if compare_format == "equal":
            test_result_status = self.compair_dict(expected_response, response)
            return test_result_status, 'check successfully' if response == expected_response else 'didnt match'

        if compare_format == "format_checking":
            if not isinstance(response, dict):
                return False, 'response must be json or dict type'

            if isinstance(expected_response, dict):

                for key, expected_value in expected_response.items():
                    if key in response and response[key] is None:
                        continue

                    if key not in response:
                        return False, f'key [{key}] didnt exist in response'

                    if not isinstance(response[key], type(expected_value)):
                        return False, (f'wrong format response format -> [{type(response[key])}] -'
                                       f' expected format -> [{type(expected_value)}]')

                    if isinstance(expected_value, dict):
                        if not self._validate_response_data(response[key], expected_value, compare_format):
                            return False, 'sub-dict didnt match'

            elif isinstance(expected_response, list):

                if len(expected_response) != len(response):
                    return False, 'list data length didnt match'

                for idx in range(len(expected_response)):

                    if type(expected_response[idx]) != type(response[idx]):
                        return False, 'type didnt match'

                    if isinstance(expected_response[idx], dict):
                        if not self._validate_response_data(response[idx], expected_response[idx], compare_format):
                            return False, 'sub-list items dict didnt match'

            return True, ''

        raise ValueError(f"Unsupported compare_format: {compare_format}")

    def compair_dict(self, x: [dict, list], y: [dict, list]) -> bool:

        """
        compair two dict

        Args:
            x: first dict
            y: second dict

        Returns:
            bool: compair result status

        """

        if type(x) != type(y):
            return False

        elif isinstance(x, dict):

            for key, value in x.items():

                if 'id' in key:
                    continue

                if type(x[key]) != type(y[key]):
                    return False

                if key not in y:
                    return False

                if isinstance(value, (dict, list)):
                    if not self.compair_dict(x[key], y[key]):
                        return False

                elif x[key] != y[key]:
                    return False

        elif isinstance(x, list):

            if len(x) != len(y):
                return False

            for idx in range(len(x)):

                if type(x[idx]) != type(y[idx]):
                    return False

                if isinstance(x[idx], (dict, list)):
                    if not self.compair_dict(x[idx], y[idx]):
                        return False

                elif x[idx] != y[idx]:
                    return False

        else:
            return False

        return True

    def _generate_report(self, validation_result: Dict[str, Any]) -> str:
        """Generate a formatted test report.

        Args:
            validation_result (Dict[str, Any]): Validation result dictionary.

        Returns:
            str: Formatted report string with emojis for visual feedback.
        """

        body_response = str(validation_result['response_body'])
        body_response = "we can't show html response" if '<!DOCTYPE html>' in body_response else body_response

        # bs4 = BeautifulSoup(body_response, 'html.parser')

        endpoint = self.endpoint
        if not validation_result["is_status_code_valid"]:
            return (
                f"\n❌ Test FAILED for endpoint: `{validation_result['method']}:{endpoint}` 🔴\n"
                f"   ➤ Expected status code: `{validation_result['expected_status_code']}`\n"
                f"   ➤ Got: `{validation_result['response_status_code']}`\n"
                f"   ➤ Error description: {validation_result['validation_description']}\n"
                f"   ➤ Response: {body_response}\n"
            )

        if not validation_result["is_body_valid"]:
            return (
                f"\n❌ Test FAILED for endpoint: `{validation_result['method']}:{endpoint}` 🔴\n"
                f"   ➤ Reason: Response body does not match expected format \n"
                f"   ➤ Error description: {validation_result['validation_description']}\n"
                f"   ➤ Response: {body_response}\n"
                f"   ➤ Expected Response: {validation_result['expected_body']}\n"
            )

        return (
            f"\n✅ Test PASSED for endpoint: `{validation_result['method']}:{endpoint}` 🟢\n"
            f"   ➤ Status code: `{validation_result['response_status_code']}`\n"
        )
