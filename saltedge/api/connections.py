from typing import TypedDict, Literal, Iterator

from saltedge.api import ListAPI, RetrieveAPI, BaseAPI, RP
from saltedge.api.attempts import AttemptDTO


class ConnectionDTO(TypedDict):
    id: str
    provider_id: str
    provider_code: str
    provider_name: str
    daily_refresh: bool
    customer_id: str
    created_at: str
    updated_at: str
    last_success_at: str
    status: Literal["active", "inactive", "disabled"]
    country_code: str
    next_refresh_possible_at: str
    last_attempt: AttemptDTO
    show_consent_confirmation: bool
    last_consent_id: str


class ConnectionAPI(
    ListAPI[ConnectionDTO], RetrieveAPI[ConnectionDTO], BaseAPI
):
    _path = "connections"
    _response_dto_class = ConnectionDTO

    def list(self, customer_id: str, **kwargs) -> Iterator[ConnectionDTO]:
        return super().list(customer_id=customer_id, **kwargs)
    
    def show(self, connection_id: str, *args, **kwargs) -> ConnectionDTO:
        return super().show(connection_id)
