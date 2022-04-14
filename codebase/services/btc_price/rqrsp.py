from pydantic import BaseModel
from datetime import datetime

class GetBtcPriceQuoteResponse(BaseModel):
    timestamp: datetime
    currency: str
    rate: str