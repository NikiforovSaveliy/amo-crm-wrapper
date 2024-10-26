import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from typing_extensions import TypeVar, Literal

from amopy.helpers.token_storages import AbstractTokenStorage

TokenStorageType = TypeVar("TokenStorageType", bound=AbstractTokenStorage)


class AbstractRequestHelper(ABC):

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


class UrlLibRequestHelper(AbstractRequestHelper):

    def request(
        self,
        method: Literal["POST", "PUT", "PATCH", "GET"],
        url: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        headers.update({"Content-Type": "application/json"})
        headers.update(self.token_storage.get_auth_header())
        json_body = json.dumps(data, default=str)
        base_url = self.get_url(url, params)
        request = Request(
            base_url,
            data=json_body.encode(),
            method=method,
            headers=headers,
        )
        response = urlopen(request)
        response_data = json.loads(response.read())
        return response_data

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
