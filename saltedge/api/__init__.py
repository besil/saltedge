from abc import ABC
from typing import (
    Iterator,
    TypeVar,
    Generic,
    TypedDict,
    Any,
    Union,
    Iterable,
    Type,
)

from saltedge.http import SaltedgeHttpClient

RQ = TypeVar("RQ")  # Request Payload
RP = TypeVar("RP")  # Response payload


class BaseAPI(ABC, Generic[RQ]):
    _path: str
    _client: SaltedgeHttpClient
    _base_url: str
    _request_dto_class: Type[RQ]
    _response_dto_class: Type[RP]

    def __init__(
        self,
        client: SaltedgeHttpClient,
        base_url: str,
    ):
        self._client = client
        self._base_url = base_url


class ListAPI(BaseAPI, Generic[RP]):
    # _list_dto_class: Type[RP]

    def list(self, **kwargs) -> Iterator[RP]:
        # dto_class = (
        #     self._list_dto_class
        #     if hasattr(self, "_list_dto_class")
        #     else self._response_dto_class
        # )
        dto_class = self._response_dto_class
        query_params = kwargs or dict()
        for payload in self._client.get(
            f"{self._base_url}/{self._path}", query_params=query_params
        ):
            for data in payload["data"]:
                yield dto_class(**data)


class RetrieveAPI(BaseAPI, Generic[RP]):
    # _retrieve_dto_class: Type[RP]

    def show(self, *args, **kwargs) -> RP:
        # dto_class = (
        #     self._retrieve_dto_class
        #     if hasattr(self, "_retrieve_dto_class")
        #     else self._response_dto_class
        # )
        dto_class = self._response_dto_class
        path_params = "/".join([arg for arg in args if arg is not None]) or ""
        query_params = kwargs or dict()
        resp = list(
            self._client.get(
                f"{self._base_url}/{self._path}/" + path_params,
                query_params=query_params,
            )
        )[0]
        return dto_class(**resp["data"])


class CreateAPI(BaseAPI, Generic[RQ, RP]):
    # _create_dto_class: Type[RP]

    def create(self, payload: RQ, *args, **kwargs) -> RP:
        # dto_class = (
        #     self._create_dto_class
        #     if hasattr(self, "_create_dto_class")
        #     else self._request_dto_class
        # )
        dto_class = self._response_dto_class
        payload = list(
            self._client.post(
                f"{self._base_url}/{self._path}/", payload={'data': payload}
            )
        )[0]
        return dto_class(**payload["data"])
        # for data in payload["data"]:
        #     yield dto_class(**data)
