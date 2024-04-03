from typing import TypedDict, Literal, NotRequired


class StageDTO(TypedDict):
    created_at: str
    id: str
    name: Literal[
        "start",
        "connect",
        "interactive",
        "fetch_holder_info",
        "fetch_accounts",
        "fetch_recent",
        "fetch_full",
        "disconnect",
        "finish",
    ]
    updated_at: str


class AttemptDTO(TypedDict):
    api_mode: Literal["app", "service"]
    api_version: str
    automatic_fetch: bool
    daily_refresh: bool
    categorization: NotRequired[Literal["none", "personal", "business"]]
    created_at: str
    custom_fields: dict
    device_type: Literal["desktop", "tablet", "mobile"]
    remote_ip: str
    customer_last_logged_at: str
    fail_at: str
    fail_error_class: str
    fail_message: str
    fetch_scopes: list[
        Literal[
            "accounts",
            "holder_info",
            "transactions",
            "accounts_without_balance",
        ]
    ]
    finished: bool
    finished_recent: bool
    from_date: str
    id: str
    interactive: bool
    locale: Literal[
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
    partial: bool
    success_at: str
    to_date: str
    updated_at: str
    show_consent_confirmation: bool
    include_natures: list[str]
    stages: list[StageDTO]
    unduplication_strategy: Literal[
        "mark_as_pending", "mark_as_duplicate", "delete_transactions"
    ]
