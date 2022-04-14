import datetime
from uuid import UUID
import uuid
from model.common import MAX_BUY_ORDER_SIZE_EXCLUSIVE_ANY_CURRENCY_UNIT, SUPPORTED_CURRENCIES
from pydantic import BaseModel, validator
from decimal import Decimal

class CreateBuyOrderRequest(BaseModel):
    currency: str
    amount: str
    idempotence_key: UUID

    @validator('currency')
    def currency_must_be_valid(cls, v):
        if v not in SUPPORTED_CURRENCIES:
            raise ValueError(f'invalid currency. valid currencies: {", ".join(SUPPORTED_CURRENCIES)}')
        return v

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if Decimal(v) <= 0:
            raise ValueError('invalid amount. amount must be positive.')
        return v

    @validator('amount')
    def amount_must_be_less_than_maximum(cls, v):
        if Decimal(v) >= MAX_BUY_ORDER_SIZE_EXCLUSIVE_ANY_CURRENCY_UNIT:
            raise ValueError(
                f'invalid amount. amount must be less than {MAX_BUY_ORDER_SIZE_EXCLUSIVE_ANY_CURRENCY_UNIT}')
        return v

class BuyOrderExport(BaseModel):
    id: uuid.UUID
    created_at: datetime.datetime
    currency: str
    currency_amount: str
    btc_rate: str
    btc_amount: str

class CreateBuyOrderResponse(BaseModel):
    idempotence_key: uuid.UUID
    buy_order: BuyOrderExport