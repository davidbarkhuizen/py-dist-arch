from pydantic import BaseModel
from uuid import UUID
import datetime

from decimal import Decimal

class BuyOrderDTO(BaseModel):
    
    id: int
    client_id: int
    external_id: UUID
    created_at: datetime.datetime
    
    currency_id: int
    currency_iso3: str
    
    currency_amount: Decimal
    btc_rate: Decimal
    btc_amount: Decimal