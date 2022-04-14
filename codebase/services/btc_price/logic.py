from typing import Optional
from model.common import SUPPORTED_CURRENCIES
from datetime import datetime
from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from model.logevent import BtcPriceRequested, BtcPriceQuoted
from services.btc_price.rqrsp import GetBtcPriceQuoteResponse
from util.coinbase import CoinBaseClient
from util.events import log_event

api = FastAPI()

coinbase_client: Optional[CoinBaseClient] = None
def configure_logic(coinbase_client_: CoinBaseClient):
    global coinbase_client
    coinbase_client = coinbase_client_

def rq_received_logevent(client_id: int, currency: str):
    return BtcPriceRequested(
        currency = currency
    )

def handle_request(client_id: int, currency: str):

    if currency not in SUPPORTED_CURRENCIES:
        raise HTTPException(status_code=400, detail=f'unsupported currency: {currency}.  supported: {", ".join(SUPPORTED_CURRENCIES)}')

    quote = coinbase_client.fetch_btc_price_quote('buy', currency)

    rsp = GetBtcPriceQuoteResponse(
        timestamp = datetime.utcnow(),
        currency = quote.currency,
        rate = quote.amount
    )

    # mock_rate = {
    #     'USD': '48478.88',
    #     'EUR': '41191.91',
    #     'GBP': '35330.89'
    # }
    
    # rsp = GetBtcPriceQuoteResponse(
    #     timestamp = datetime.utcnow(),
    #     currency = currency,
    #     rate = mock_rate[currency]        
    # )

    log_event(
        BtcPriceQuoted(
            source='coinbase',
            timestamp=rsp.timestamp.isoformat(),
            currency=rsp.currency,
            rate=rsp.rate
        )
    )

    return rsp