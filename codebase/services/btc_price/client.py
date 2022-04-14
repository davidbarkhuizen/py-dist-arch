from util.web import url_for_endpoint
from model.common import Endpoint
from services.btc_price.rqrsp import GetBtcPriceQuoteResponse
import requests

class BtcPriceServiceClient:

    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    def get_buy_price(self, currency: str):

        url = f'{url_for_endpoint(self.endpoint)}/buy'
        print(url)
        http_rsp = requests.get(url, { 'currency': currency })

        if http_rsp.status_code != 200:
            raise f'get buy price error: {http_rsp.text}'

        return GetBtcPriceQuoteResponse.parse_raw(http_rsp.text).rate
    