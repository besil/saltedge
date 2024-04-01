from abc import ABC
from typing import Iterator, TypeVar, Generic

from saltedge.http import SaltedgeHttpClient

T = TypeVar("T")


class BaseAPI(ABC, Generic[T]):
    _path: str
    _client: SaltedgeHttpClient
    _base_url: str
    _dto_class: T

    def __init__(
        self,
        client: SaltedgeHttpClient,
        base_url: str,
    ):
        self._client = client
        self._base_url = base_url


class ListAPI(BaseAPI, Generic[T]):
    _list_dto_class: T

    def list(self, **kwargs) -> Iterator[T]:
        dto_class = self._list_dto_class if hasattr(self, '_list_dto_class') else self._dto_class
        query_params = kwargs or dict()
        for payload in self._client.get(
            f"{self._base_url}/{self._path}", query_params=query_params
        ):
            for data in payload["data"]:
                yield dto_class(**data)


class RetrieveAPI(BaseAPI, Generic[T]):
    _retrieve_dto_class: T

    def show(self, *args, **kwargs) -> T:
        dto_class = self._retrieve_dto_class if hasattr(self, '_retrieve_dto_class') else self._dto_class
        path_params = "/".join([arg for arg in args if arg is not None]) or ""
        query_params = kwargs or dict()
        for payload in self._client.get(
            f"{self._base_url}/{self._path}/" + path_params,
            query_params=query_params,
        ):
            for data in payload["data"]:
                yield dto_class(**data)
