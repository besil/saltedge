import datetime as dt
from typing import TypedDict, NotRequired, Literal

from saltedge.api import CreateAPI, DeleteAPI, BaseAPI


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


class DeletedLeadResponseDTO(TypedDict):
    deleted: bool
    lead_email: str


class LeadsAPI:
    class CreateLeadsAPI(
        CreateAPI[CreatedLeadResponseDTO], BaseAPI
    ):
        _path = "leads"
        _response_dto_class = CreatedLeadResponseDTO

        # def create(self, payload: CreateLeadDTO, *args, **kwargs) -> CreatedLeadResponseDTO:
        #     return super().create(payload)

    class DeleteLeadsAPI(DeleteAPI[DeletedLeadResponseDTO], BaseAPI):
        _path = "leads"
        _response_dto_class = DeletedLeadResponseDTO

    def __init__(self, client, base_url):
        super().__init__()
        self._create_api = self.CreateLeadsAPI(client, base_url=base_url)
        self._delete_api = self.DeleteLeadsAPI(client, base_url=base_url)

    def create(self, payload: CreateLeadDTO) -> CreatedLeadResponseDTO:
        return self._create_api.create(payload=payload)

    def delete(self, customer_id: str) -> DeletedLeadResponseDTO:
        return self._delete_api.delete(customer_id=customer_id)
