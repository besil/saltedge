from typing import TypedDict, Literal, NotRequired

from saltedge.api import CreateAPI, BaseAPI
from saltedge.logging import log


class KycDTO(TypedDict):
    type_of_account: NotRequired[Literal["own", "legal", "shared"]]


ALL_CONSENTS = [
    "account_details",
    # "holder_information",
    "transactions_details",
]


class ConsentDTO(TypedDict):
    # valid combinations are:
    # ["account_details"],
    # ["holder_information"],
    # ["account_details", "holder_information"],
    # ["account_details", "transactions_details"],
    # ["account_details", "holder_information", "transactions_details"],
    scopes: list[
        Literal[
            "account_details", "holder_information", "transactions_details"
        ]
    ]
    from_date: NotRequired[str]  # 2024-03-01, with 365 days ago
    to_date: NotRequired[str]  # 2024-03-01
    period_days: NotRequired[int]


class AttemptDTO(TypedDict):
    # valid combinations are:
    # ['accounts'],
    # ['holder_info'],
    # ['accounts', 'holder_info'],
    # ['accounts', 'transactions'],
    # ['accounts', 'holder_info', 'transactions'],
    # ['accounts_without_balance'],
    # ['accounts_without_balance', 'holder_info']
    fetch_scopes: NotRequired[
        list[
            Literal[
                "accounts",
                "holder_info",
                "transactions",
                "accounts_without_balance",
            ]
        ]
    ]
    from_date: NotRequired[str]  # 2024-03-01, with 365 days ago
    to_date: NotRequired[str]  # 2024-03-01
    fetched_accounts_notify: NotRequired[bool]
    custom_fields: NotRequired[dict]
    locale: NotRequired[
        Literal[
            "bg",
            "cz",
            "de",
            "en",
            "es-MX",
            "es",
            "fi",
            "fr",
            "he",
            "hr",
            "hu",
            "it",
            "nl",
            "pl",
            "pt-BR",
            "pt",
            "ro",
            "ru",
            "si",
            "sk",
            "sv",
            "tr",
            "uk",
            "zh-HK",
            "zh",
        ]
    ]
    include_natures: NotRequired[
        list[
            Literal[
                "account",
                "bonus",
                "card",
                "checking",
                "credit",
                "credit_card",
                "debit_card",
                "ewallet",
                "insurance",
                "investment",
                "loan",
                "mortgage",
                "savings",
            ]
        ]
    ]
    customer_last_logged_at: NotRequired[str]  # datetime
    unduplication_strategy: NotRequired[
        Literal["mark_as_pending", "mark_as_duplicate", "delete_transactions"]
    ]
    return_to: NotRequired[str]


class LeadSessionDTO(TypedDict):
    customer_id: NotRequired[str]
    consent: ConsentDTO
    attempt: NotRequired[AttemptDTO]
    allowed_countries: NotRequired[
        list[
            Literal[
                "AT",
                "BE",
                "BG",
                "CY",
                "CZ",
                "DE",
                "DK",
                "EE",
                "ES",
                "FI",
                "FR",
                "GB",
                "GR",
                "HR",
                "HU",
                "IE",
                "IS",
                "IT",
                "LI",
                "LT",
                "LU",
                "LV",
                "MT",
                "NL",
                "NO",
                "PL",
                "PT",
                "RO",
                "SE",
                "SI",
                "SK",
                "XF",
            ]
        ]
    ]
    country_code: NotRequired[str]
    provider_code: NotRequired[str]
    skip_provider_select: NotRequired[bool]
    daily_refresh: NotRequired[bool]
    disable_provider_search: NotRequired[bool]
    return_connection_id: NotRequired[bool]
    provider_modes: NotRequired[list[Literal["oauth", "web", "api", "file"]]]
    categorization: NotRequired[list[Literal["none", "personal", "business"]]]
    include_fake_providers: NotRequired[bool]
    return_error_class: NotRequired[bool]
    regulated: NotRequired[bool]
    theme: NotRequired[Literal["default", "dark"]]
    connect_template: NotRequired[str]
    javascript_callback_type: NotRequired[Literal["post_message"]]
    kyc: NotRequired[KycDTO]


class LeadSessionCreatedResponseDTO(TypedDict):
    expires_at: str
    redirect_url: str


class LeadSessionCreateAPI(CreateAPI[LeadSessionCreatedResponseDTO]):
    _path = "lead_sessions/create"
    _response_dto_class = LeadSessionCreatedResponseDTO

    def create(
        self, payload: LeadSessionDTO, *args, **kwargs
    ) -> LeadSessionCreatedResponseDTO:
        return super().create(payload)


class LeadSessionAPI:
    def __init__(self, client, base_url):
        self._create_api = LeadSessionCreateAPI(client, base_url=base_url)

    def create(self, payload: LeadSessionDTO) -> LeadSessionCreatedResponseDTO:
        log.debug("Create a lead")
        return self._create_api.create(payload=payload)

    def reconnect(self):
        raise NotImplementedError()

    def refresh(self):
        raise NotImplementedError()
