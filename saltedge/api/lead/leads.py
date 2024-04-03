import datetime as dt
from typing import TypedDict, NotRequired, Literal, Iterator

from saltedge.api import CreateAPI, BaseAPI, RQ, RP


class KycDTO(TypedDict):
    full_name: NotRequired[str]
    type_of_account: NotRequired[Literal["own", "legal", "shared"]]
    citizenship_code: NotRequired[str]
    residence_address: NotRequired[str]
    date_of_birth: NotRequired[dt.date]
    gender: NotRequired[Literal["male", "female", "other"]]
    legal_name: NotRequired[str]
    registered_office_code: NotRequired[str]
    registered_office_address: NotRequired[str]
    registration_number: NotRequired[str]


class CreateLeadDTO(TypedDict):
    email: str
    identifier: NotRequired[str]
    kyc: NotRequired[KycDTO]


class CreatedLeadResponseDTO(TypedDict):
    email: str
    customer_id: str
    identifier: str


class LeadsAPI(CreateAPI[CreateLeadDTO, CreatedLeadResponseDTO], BaseAPI):
    _path = "leads"
    _response_dto_class = CreatedLeadResponseDTO

    def create(self, payload: CreateLeadDTO, *args, **kwargs) -> CreatedLeadResponseDTO:
        return super().create(payload)
