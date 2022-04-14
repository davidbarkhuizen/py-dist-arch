from enum import Enum
from typing import Optional

MAX_BUY_ORDER_SIZE_EXCLUSIVE_ANY_CURRENCY_UNIT = 1000000000
BUY_ORDER_BOOK_THRESHOLD_BTC = 1000000

BTC_RATE_PRECISION = 40
BTC_RATE_SCALE = 20

class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'

SUPPORTED_CURRENCIES = [Currency.USD.value, Currency.EUR.value, Currency.GBP.value]

class Queue(Enum):
    BuyOrder = 'buy_order'
   
EXCHANGE = ''

QUEUE_NAMES = [(q.value) for q in Queue]

class Service(Enum):
    CREATE_BUY_ORDER = 'create_buy_order'
    FETCH_BUY_ORDERS = 'fetch_buy_orders'
    BTC_PRICE = 'btc_price'
    MIGRATION = 'migration'
    READ_MODEL_SYNC = 'read_model_sync'

from model.common import Queue
from pydantic import BaseModel

class Endpoint(BaseModel):
    protocol: str
    host: str
    port: int
    path: Optional[str] = None
    retry_wait_s: int = 1

class DatabaseEndPoint(Endpoint):
    host: str
    port: int
    database: str
    user: str
    pwd: str

class QueueEndpoint(BaseModel):
    host: str
    port: int
    exchange: str
    queue: Queue
    retry_wait_s: int = 1