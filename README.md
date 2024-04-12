# Saltedge python sdk
A simple python wrapper around [saltedge](https://docs.saltedge.com/general/) api with some utilities.

## Features
- Automatic page handling through generators
- Modular design
- Dynamic payload with typing support with TypedDict

# Quickstart 

## Installation
```
pip install saltedge
```

## Partner API overview (AISP)
https://docs.saltedge.com/partners/v1/#quick_start
```python
import datetime as dt

from saltedge.api.accounts import AccountDTO
from saltedge.api.connections import ConnectionDTO
from saltedge.api.lead.leads import CreateLeadDTO
from saltedge.api.lead.sessions import (
    LeadSessionDTO,
    ConsentDTO,
    ALL_CONSENTS,
    AttemptDTO,
)
from saltedge.api.transactions import TransactionDTO
from saltedge.http import SaltedgeHttpClient
from saltedge.services import PartnersAccountService

# your saltedge credentials
app_id = "<your app id>"
app_secret = "<your app secret"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n...\n-----END PRIVATE KEY-----".encode(
    "utf-8"
)
client = SaltedgeHttpClient(app_id, app_secret, private_key)
partner:PartnersAccountService = PartnersAccountService(client)

# Create a lead
resp = partner.leads.create(payload=CreateLeadDTO(email="foo@example.com"))
print(resp)
# {'email': 'foo@example.com', 'customer_id': '123456.....'}

customer_id = resp["customer_id"]
# Create a Lead session
resp = partner.lead_session.create(
    payload=LeadSessionDTO(
        attempt=AttemptDTO(
            return_to="https://localhost",
        ),
        country_code="IT",
        # ... many other options here. see docs: https://docs.saltedge.com/partners/v1/#lead_sessions-create
        customer_id=customer_id,
        consent=ConsentDTO(
            scopes=ALL_CONSENTS,
            from_date=(dt.date.today() - dt.timedelta(days=365)).strftime(
                "%Y-%m-%d"
            ),
        ),
    )
)
print(resp)
# {'expires_at': '2024-04-12T07:37:14Z', 'redirect_url': 'https://www.saltedge.com/dashboard/connect?token=123'}

# After visiting connect_link and connecting with your bank,
# you will be able to fetch data

# List connection
connection: ConnectionDTO
for connection in partner.connections.list(customer_id):
    print(connection)

# Show details
connection = list(partner.connections.list(customer_id))[0]
print(partner.connections.show(connection["id"]))
# {'id': '123', 'secret': '123', 'provider_id': '123', 'provider_code': 'fake_demobank_xf', 'provider_name': 'Fake Demo Bank', 'customer_id': '123', 'status': 'active', 'categorization': '...'}

# List transactions
transaction: TransactionDTO
for transaction in partner.transactions.list(connection_id=connection["id"]):
    print(transaction)
# {'id': '123', 'account_id': '123', 'duplicated': False, 'mode': 'normal', 'status': 'posted', 'made_on': '2024-03-01', 'amount': -64.0, 'currency_code': 'USD', 'description': 'ADOBE CREATIVE Debit IRELAND ON 28 FEB BDC', 'category': 'electronics_and_software', 'extra': {'merchant_id': '3847a91cad0519323b364fa6e83590110657a7c89f4775eaec89169f82b197ae', 'account_balance_snapshot': 314.58, 'categorization_confidence': 1}, 'created_at': '2024-04-12T07:42:10Z', 'updated_at': '2024-04-12T07:42:10Z'}

# List accounts
account: AccountDTO
for account in partner.accounts.list(connection["id"]):
    print(account)
# {'id': '123', 'connection_id': '123', 'name': 'Current Account', 'nature': 'account', 'balance': 314.58, 'currency_code': 'USD', 'extra': {'iban': 'DE1234567890987654321123', 'swift': 'ABCDEFGH', 'status': 'active', 'sort_code': '65-43-21', 'client_name': 'John Smith', 'account_name': 'Current Account', 'account_number': '123456', 'available_amount': 314.58, 'transactions_count': {'posted': 38, 'pending': 0}, 'last_posted_transaction_id': '1252994279446415881'}, 'created_at': '2024-04-12T07:42:08Z', 'updated_at': '2024-04-12T07:42:14Z'}
```


# How to contribute
## Dependencies
- python 3.11+
- poetry

## Dev quickstart
```shell
git clone git@github.com:besil/saltedge.git
cd saltedge
poetry install
```
