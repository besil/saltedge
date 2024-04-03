from typing import TypedDict, Literal, NotRequired, Iterator

from saltedge.api import ListAPI, BaseAPI, RP
from saltedge.http import SaltedgeHttpClient


class TransactionExtraDTO(TypedDict):
    account_balance_snapshot: NotRequired[float]
    account_number: NotRequired[str]
    additional: NotRequired[str]
    asset_amount: NotRequired[float]
    asset_code: NotRequired[str]
    categorization_confidence: NotRequired[float]
    check_number: NotRequired[str]
    closing_balance: NotRequired[float]
    constant_code: NotRequired[str]
    convert: NotRequired[bool]
    customer_category_code: NotRequired[str]
    customer_category_name: NotRequired[str]
    exchange_rate: NotRequired[float]
    id: NotRequired[str]
    end_to_end_id: NotRequired[str]
    information: NotRequired[str]
    mcc: NotRequired[str]
    merchant_id: NotRequired[str]
    opening_balance: NotRequired[float]
    installment_debt_amount: NotRequired[float]
    original_amount: NotRequired[float]
    original_category: NotRequired[str]
    original_currency_code: NotRequired[str]
    original_subcategory: NotRequired[str]
    payee: NotRequired[str]
    payee_information: NotRequired[str]
    payer: NotRequired[str]
    payer_information: NotRequired[str]
    possible_duplicate: NotRequired[bool]
    posted_by_aspsp: NotRequired[bool]
    posting_date: NotRequired[str]
    posting_time: NotRequired[str]
    record_number: NotRequired[str]
    specific_code: NotRequired[str]
    tags: NotRequired[list[str]]
    time: NotRequired[str]
    transfer_account_name: NotRequired[str]
    type: NotRequired[str]
    unit_price: NotRequired[float]
    units: NotRequired[float]
    variable_code: NotRequired[str]


class TransactionDTO(TypedDict):
    id: str
    mode: Literal["normal", "fee", "transfer"]
    status: Literal["posted", "pending"]
    made_on: str
    amount: float
    currency_code: str
    description: str
    category: str
    duplicated: bool
    extra: NotRequired[TransactionExtraDTO]
    account_id: str
    created_at: str
    updated_at: str


class TransactionAPI:
    class TransactionListAPI(ListAPI[TransactionDTO], BaseAPI):
        _path = "transactions"
        _response_dto_class = TransactionDTO

        def list(
            self, connection_id: str, account_id: str = None, **kwargs
        ) -> Iterator[TransactionDTO]:
            params = {"connection_id": connection_id}
            if account_id:
                params |= {"account_id": account_id}
            return super().list(**params)

    class TransactionPendingAPI(TransactionListAPI):
        _path = "transactions/pending"

    class TransactionDuplicatesAPI(TransactionListAPI):
        _path = "transactions/duplicates"

    def __init__(self, client: SaltedgeHttpClient, base_url: str):
        self._transactions = self.TransactionListAPI(client, base_url)
        self._pending = self.TransactionPendingAPI(client, base_url)
        self._duplicates = self.TransactionDuplicatesAPI(client, base_url)

    def list(self, connection_id: str, account_id: str = None):
        return self._transactions.list(connection_id, account_id=account_id)

    def pending(self, connection_id: str, account_id: str = None):
        return self._pending.list(connection_id, account_id=account_id)

    def duplicates(self, connection_id: str, account_id: str = None):
        return self._duplicates.list(connection_id, account_id=account_id)
