import datetime as dt
from typing import TypedDict, Optional, Literal


class KycDTO(TypedDict):
    full_name: Optional[str]
    type_of_account: Optional[Literal["own", "legal", "shared"]]
    citizenship_code: Optional[str]
    residence_address: Optional[str]
    date_of_birth: Optional[dt.date]
    gender: Optional[Literal["male", "female", "other"]]
    legal_name: Optional[str]
    registered_office_code: Optional[str]
    registered_office_address: Optional[str]
    registration_number: Optional[str]


class CreateLeadDTO(TypedDict):
    email: str
    identifier: Optional[str]
    kyc: Optional[KycDTO]
