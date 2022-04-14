from util.service import request_handler
from services.create_buy_order.logic import configure_logic, handle_create_buy_order_request, rq_received_logevent

from sqlalchemy.engine.base import Engine
from services.btc_price.client import BtcPriceServiceClient
from util.events import log_event

from fastapi import FastAPI

from services.create_buy_order.rqrsp import CreateBuyOrderRequest
from model.logevent import HealthChecked

def configure_api(write_engine: Engine, q_publisher, btc_price_service: BtcPriceServiceClient):
    configure_logic(write_engine, q_publisher, btc_price_service)

api = FastAPI()

@api.get("/healthcheck")
async def get_root():
    log_event(HealthChecked())

@api.put("/buy_order")
def create_buy_order(rq: CreateBuyOrderRequest):
    return request_handler(
        'CreateBuyOrderRequestReceived', 
        rq_received_logevent, 
        handle_create_buy_order_request
    )(rq)