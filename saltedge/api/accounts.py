import datetime as dt
from typing import Literal, TypedDict, Iterator

from saltedge.api import ListAPI, BaseAPI, RP


class FloatingInterestRateDTO(TypedDict):
    min_value: float
    max_value: float


class AccountExtraDTO(TypedDict):
    account_name: str
    account_number: str
    assets: list[dict]
    available_amount: float
    balance_type: str
    blocked_amount: float
    card_type: Literal[
        "american_express",
        "china_unionpay",
        "diners_club",
        "jcb",
        "maestro",
        "master_card",
        "uatp",
        "visa",
        "mir",
    ]
    cards: list[str]
    client_name: str
    closing_balance: float
    credit_limit: float
    current_date: dt.date
    current_time: dt.datetime
    expiry_date: dt.date
    iban: str
    bban: str
    interest_rate: float
    interest_type: str
    floating_interest_rate: FloatingInterestRateDTO
    remaining_payments: float
    penalty_amount: float
    next_payment_amount: float
    next_payment_date: dt.date
    open_date: dt.date
    opening_balance: float  # Assuming opening_balance also uses float
    partial: bool
    provider_account_id: str
    raw_balance: str
    sort_code: str
    statement_cut_date: dt.date
    status: str
    swift: str
    total_payment_amount: dt.date
    transactions_count: dict
    payment_type: str
    cashback_amount: float


class AccountDTO(TypedDict):
    id: str
    name: str
    nature: Literal[
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
    balance: float
    currency_code: str
    extra: AccountExtraDTO
    connection_id: str
    created_at: str
    updated_at: str


class AccountAPI(ListAPI[AccountDTO], BaseAPI):
    _path = "accounts"
    _response_dto_class = AccountDTO

    def list(
        self, connection_id: str = None, customer_id: str = None
    ) -> Iterator[AccountDTO]:
        params = dict()
        match (connection_id, customer_id):
            case (None, None):
                raise ValueError(
                    "Connection_id and customer_id can't be both None"
                )
            case x, None if x is not None:
                params["connection_id"] = x
            case None, y if y is not None:
                params["customer_id"] = y
            case x, y if x is not None and y is not None:
                params["connection_id"] = x
        return super().list(**params)
