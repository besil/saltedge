import datetime as dt
from typing import TypedDict, Literal, Any

from saltedge.api import ListAPI, BaseAPI, RetrieveAPI, CreateAPI, BaseAPI


class ProviderDTO(TypedDict):
    id: str
    code: str
    name: str
    mode: Literal["oauth", "web", "api", "file"]
    status: Literal["active", "inactive", "disabled"]
    automatic_fetch: bool
    dynamic_registration_code: str
    group_code: str
    group_name: str
    hub: str
    customer_notified_on_sign_in: bool
    interactive: bool
    instruction: str
    home_url: str
    login_url: str
    logo_url: str
    country_code: str
    refresh_timeout: int
    holder_info: list
    max_consent_days: int
    created_at: dt.datetime
    updated_at: dt.datetime
    timezone: str
    max_interactive_delay: int
    optional_interactivity: bool
    regulated: bool
    max_fetch_interval: int
    custom_pendings: bool
    custom_pendings_period: int
    supported_fetch_scopes: list[str]
    supported_account_extra_fields: list[str]
    supported_transaction_extra_fields: list[str]
    supported_account_natures: list[str]
    supported_account_types: Literal["personal", "business"]
    identification_codes: list[str]
    bic_codes: list[str]
    supported_iframe_embedding: Literal["true", "false"]
    payment_templates: list[str]
    supported_payment_fields: dict[str, Any]
    required_payment_fields: dict[str, Any]
    no_funds_rejection_supported: bool


class ProviderAPI(ListAPI[ProviderDTO], RetrieveAPI[ProviderDTO], BaseAPI):
    _path = "providers"
    _response_dto_class = ProviderDTO

    def show(self, code: str = None, *args, **kwargs) -> ProviderDTO:
        return super().show(code)

