from abc import ABC

from saltedge.api.connections import ConnectionAPI
from saltedge.api.countries import CountriesAPI
from saltedge.api.lead.leads import LeadsAPI
from saltedge.api.accounts import AccountAPI
from saltedge.api.lead.sessions import LeadSessionAPI
from saltedge.api.providers import ProviderAPI
from saltedge.api.transactions import TransactionAPI
from saltedge.http import SaltedgeHttpClient


class BaseSaltedgeService(ABC):
    client: SaltedgeHttpClient
    base_url: str = "https://www.saltedge.com/api"

    def __init__(self, client: SaltedgeHttpClient):
        self.client = client
        self.countries = CountriesAPI(client, self.base_url)
        self.providers = ProviderAPI(client, self.base_url)
        self.leads = LeadsAPI(client, self.base_url)
        self.lead_session = LeadSessionAPI(client, self.base_url)
        self.connections = ConnectionAPI(client, self.base_url)
        self.accounts = AccountAPI(client, self.base_url)
        self.transactions = TransactionAPI(client, self.base_url)


class BasePartnerService(BaseSaltedgeService):
    base_url = BaseSaltedgeService.base_url + "/partners/v1"


class PartnersAccountService(BasePartnerService):
    pass


class PartnersPaymentService(BasePartnerService):
    pass
