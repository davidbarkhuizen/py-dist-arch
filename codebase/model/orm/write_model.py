from sqlalchemy import Column, Integer, String, SMALLINT, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from model.common import BTC_RATE_SCALE, BTC_RATE_PRECISION
from model.common import SUPPORTED_CURRENCIES

supported_currencies = ",".join([f'"{x}"' for x in SUPPORTED_CURRENCIES])

WriteModelBase = declarative_base()

class Client(WriteModelBase):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    email = Column(String(254), unique=True, nullable=False)

class Currency(WriteModelBase):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    iso3 = Column(String(3), nullable=False)
    dp = Column(SMALLINT, nullable=False)

    def __repr__(self):
       return f'id {self.id}: {self.iso3} ({self.dp} DP)'

class BuyOrderRunningTotal(WriteModelBase):
    __tablename__ = 'buy_order_running_total'
    id = Column(Integer, primary_key=True)
    btc_amount  = Column(DECIMAL(precision=12, scale=8), nullable=False)

class BuyOrder(WriteModelBase):
    __tablename__ = 'buy_order'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    external_id = Column(UUID(as_uuid=True), nullable=False, server_default=text('gen_random_uuid()'))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now()) 

    currency_id = Column(ForeignKey('currency.id'), nullable=False)
    currency_amount = Column(DECIMAL(precision=12, scale=2), nullable=False)
    btc_rate = Column(DECIMAL(precision=BTC_RATE_PRECISION, scale=BTC_RATE_SCALE), nullable=False)
    btc_amount  = Column(DECIMAL(precision=11, scale=8), nullable=False)

class BuyOrderIdempotenceCache(WriteModelBase):
    __tablename__ = 'buy_order_idempotence_cache'

    client_id = Column(Integer, nullable=False)
    currency_id = Column(Integer, nullable=False)
    currency_amount = Column(DECIMAL(precision=12, scale=2), nullable=False)
    idempotence_key = Column(UUID(as_uuid=True), nullable=False)

    buy_order_id = Column(Integer, primary_key=True)