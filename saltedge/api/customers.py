from typing import TypedDict, Iterator

from saltedge.api import ListAPI, RetrieveAPI, BaseAPI, RP


class CustomerDTO(TypedDict):
    id: str
    identifier: str
    created_at: str
    updated_at: str


class CustomerAPI(ListAPI[CustomerDTO], RetrieveAPI[CustomerDTO], BaseAPI):
    _path = "customers"
    _request_dto_class = CustomerDTO

    def show(self, customer_id: int) -> CustomerDTO:
        return super().show(customer_id)
