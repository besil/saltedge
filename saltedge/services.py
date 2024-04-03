from abc import ABC

from saltedge.api.countries import CountriesAPI
from saltedge.api.lead.leads import LeadsAPI
from saltedge.api.lead.session import LeadSessionAPI
from saltedge.api.providers import ProviderAPI
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


class BasePartnerService(BaseSaltedgeService):
    base_url = BaseSaltedgeService.base_url + "/partners/v1"


class PartnersAccountService(BasePartnerService):
    pass


class PartnersPaymentService(BasePartnerService):
    pass
