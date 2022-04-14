from util.service_base import ServiceDefinition, serve
from util.env import endpoint_from_env
from util.coinbase import CoinBaseClient
from model.common import Service
from services.btc_price.service import api, configureApi

def service_definition():

    def configure_service():
        cb_endpoint = endpoint_from_env('CB')
        coinbase_client = CoinBaseClient(cb_endpoint)
        configureApi(coinbase_client)

    return ServiceDefinition(Service.BTC_PRICE, configure_service, None, api)

serve(service_definition())
