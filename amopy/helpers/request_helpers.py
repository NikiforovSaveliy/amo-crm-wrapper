import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib import request

from typing_extensions import TypeVar, Literal

from amopy.helpers.token_storages import AbstractTokenStorage

TokenStorageType = TypeVar("TokenStorageType", bound=AbstractTokenStorage)


class AbstractRequestHelper(ABC):

    allowed_statuses = [200, 201]

    def __init__(self, base_url: str, token_storage: TokenStorageType):
        self.token_storage = token_storage
        self._base_url = base_url

    @abstractmethod
    def post(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def patch(self, *args, **kwargs):
        pass

    def get_url(self, path: str, params: dict = None):
        base_url = "{}/{}".format(self._base_url, path)
        if params:
            encoded_params = urlencode(params)
            base_url += "?" + encoded_params
        return base_url


class ResponseError(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class InvalidResponseStatusError(Exception):

    def __init__(self, message, status_code=None, response_body=None):
        self._status_code = status_code
        self._response_body = response_body
        super().__init__(message)


class UrlLibRequestHelper(AbstractRequestHelper):

    def request(
        self,
        method: Literal["POST", "PUT", "PATCH", "GET"],
        url: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        headers = headers or {}
        headers.update({"Content-Type": "application/json"})
        headers.update(self.token_storage.get_auth_header())
        json_body = json.dumps(data, default=str)
        base_url = self.get_url(url, params)
        request_object = request.Request(
            base_url,
            data=json_body.encode(),
            method=method,
            headers=headers,
        )

        try:
            response = request.urlopen(request_object)

            if response.getcode() not in self.allowed_statuses:
                raise InvalidResponseStatusError(
                    "Received invalid response status code: {}".format(
                        response.getcode()
                    ),
                    status_code=response.getcode(),
                    response_body=response.read().decode("utf-8"),
                )
            response_data = json.loads(response.read())
            return response_data
        except HTTPError as e:
            raise InvalidResponseStatusError(
                "Error occurred during making request: {}".format(e)
            )
        except URLError as e:
            raise InvalidResponseStatusError(
                "Error occurred during makingg request: {}".format(e)
            )
        except json.JSONDecodeError as e:
            raise InvalidResponseStatusError(
                "Error occurred during decoding request body: {}".format(e)
            )

    def get(
        self, url: str, *, params: Optional[Dict] = None, headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        return self.request(method="GET", url=url, params=params)

    def post(
        self,
        url: str,
        *,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        return self.request(method="POST", url=url, data=data, params=params)

    def patch(
        self,
        url: str,
        *,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        return self.request(method="PATCH", url=url, data=data, params=params)
