from typing import Dict, Callable

import requests
from requests import RequestException


class CustomRequest:

    endpoint = None
    data = {}
    method = 'GET'
    token = {}
    http_only_cookie = False

    def __init__(self):
        # Supported HTTP methods mapped to their respective requests functions
        self._METHOD_MAP: Dict[str, Callable] = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "PATCH": requests.patch,
            "DELETE": requests.delete,
        }

    def _send_request(self, url: str = None, data: dict = None) -> requests.Response:
        """Send the HTTP request to the endpoint.

        Args:
            url: endpoint's url to send request to custom endpoint
            data: data that we must send to endpoint as body

        Returns:
            requests.Response: The HTTP response object.

        Raises:
            RequestException: If the request fails.
        """
        request_func = self._METHOD_MAP[self.method]
        headers, cookies = self._prepare_headers_and_cookies()

        request_kwargs = {
            "url": url if url else self.endpoint,
            "headers": headers,
            "cookies": cookies,
            "json": data if data else self.data
        }

        try:
            return request_func(**request_kwargs)
        except RequestException as e:
            raise RequestException(f"Request failed: {str(e)}")

    def _prepare_headers_and_cookies(self) -> tuple[Dict[str, str], Dict[str, str]]:
        """Prepare headers and cookies based on token configuration.

        Returns:
            tuple[Dict[str, str], Dict[str, str]]: Headers and cookies dictionaries.
        """
        headers: Dict[str, str] = {}
        cookies: Dict[str, str] = {}

        if self.token:
            access_token = self.token.get("access_token", "")
            if self.http_only_cookie:
                cookies[self.token.get("cookies_token_keyname", "token")] = access_token
            else:
                headers["Authorization"] = f"Bearer {access_token}"

        return headers, cookies
