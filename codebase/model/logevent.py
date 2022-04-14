from enum import Enum
from typing import Optional
from pydantic import BaseModel

class LoggingTag(Enum):
    Root = 'xapo'

class CreateBuyOrderRequestReceived(BaseModel):
    currency: str
    amount: str
    idempotence_key: str
    client_id: int

class CreateBuyOrderResponseReturned(BaseModel):
    external_id: str

class RequestFailed(BaseModel):
    request: str
    error: str
    reference: str

class BtcPriceRequested(BaseModel):
    currency: str

class BtcPriceQuoted(BaseModel):
    source: str
    timestamp: str
    currency: str
    rate: str

class ConnectedToDatabase(BaseModel):
    database: str
    port: str
    host: str
    user: str

class FailedToConectToDatabase(ConnectedToDatabase):
    error: str

class ServiceStarted(BaseModel):
    pass   

class ServiceShutdownExceptionOccurred(BaseModel):
    error: str

class QueueListenerFailedToConnect(BaseModel):
    queue_host: str
    queue_port: int
    queue_name: str
    error: str

class QueueListenerStartingConsumption(BaseModel):
    queue_name: str

class HealthChecked(BaseModel):
    pass

class BuyOrderReadModelSynced(BaseModel):
    id: int

class FailedToSyncBuyOrderReadModel(BaseModel):
    id: int
    info: str

class Information(BaseModel):
    text: str

class BuyOrderCreated(BaseModel):
    id: int
    external_id: str

class ServiceShutDown(BaseModel):
    exit_code: int

class DatabaseMigrated(BaseModel):
    database: str

class WaitingForMigrations(BaseModel):
    pass

class DatabaseMigrationExceptionOccurred(BaseModel):
    database: str
    info: str

class CoinbaseClientExceptionOccurred(BaseModel):
    currency: str
    price_type: str
    info: str

class BtcPriceClientFailed(BaseModel):
    currency: str

class ServiceConfigurationExceptionOccurred(BaseModel):
    info: str

class ServiceRunLogicExceptionOccurred(BaseModel):
    info: str

class ServiceWebServeExceptionOccurred(BaseModel):
    info: str

class QueuePublisherConnectionExceptionOccurred(BaseModel):
    queue: str
    info: str

class QueuePublisherFailedToConnect(BaseModel):
    queue_host: str
    queue_port: int
    queue_name: str
    info: str

class QueuePublisherConnected(BaseModel):
    queue_name: str

class ModelUpdateFailed(BaseModel):
    model: str
    info: str

class BuyOrderRequestIdempotenceCacheHit(BaseModel):
    client_id: int
    currency: str
    amount: str
    idempotence_key: str

class ErrorRetrievingBuyOrderRequestViaIdempotenceCache(BaseModel):
    client_id: int
    currency: str
    amount: str
    idempotence_key: str
    info: str

class BuyOrdersPageRequested(BaseModel):
    client_id: int
    last_reference: Optional[str]
    page_size: Optional[int]