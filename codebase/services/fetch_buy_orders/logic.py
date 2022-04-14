from util.calc import dec_str
from model.logevent import BuyOrdersPageRequested
from sqlalchemy.sql.expression import desc
from services.fetch_buy_orders.rqrsp import BuyOrderExport, BuyOrderPage
from typing import List, Optional
from model.orm.read_model import BuyOrderReadModel
from sqlalchemy.orm.session import Session
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
import uuid

read_model_engine: Optional[Engine] = None
def configure_get_buy_orders(read_model_engine_):
    global read_model_engine
    read_model_engine = read_model_engine_

def get_buy_orders_log_event(client_id: int, last_reference: str, page_size: int):
    return BuyOrdersPageRequested(
        client_id = client_id,
        last_reference = last_reference,
        page_size = page_size
    )

def handle_get_buy_orders(client_id: int, last_reference: str = None, page_size: int = 10):

    db_page: Optional[List[BuyOrderReadModel]] = None

    if last_reference:

        last_external_id = uuid.UUID(last_reference)

        last_buy_order: Optional[BuyOrderReadModel] = None
        
        with Session(read_model_engine) as db_session:
            last_buy_order = db_session.query(BuyOrderReadModel)\
                .filter(
                    BuyOrderReadModel.client_id == client_id,
                    BuyOrderReadModel.external_id == last_external_id
                ).one()
        
        with Session(read_model_engine) as db_session:            
            db_page = db_session.query(BuyOrderReadModel)\
                .filter(
                    BuyOrderReadModel.client_id == client_id,
                    BuyOrderReadModel.id > last_buy_order.id
                )\
                .order_by(desc(BuyOrderReadModel.created_at))\
                .one()

    else:

        with Session(read_model_engine) as db_session:            
            db_page = db_session.query(BuyOrderReadModel)\
                .filter(BuyOrderReadModel.client_id == client_id)\
                .order_by(desc(BuyOrderReadModel.created_at))\
                .limit(page_size)\
                .all()

    return BuyOrderPage(
        rows = [
            BuyOrderExport(
                id = rec.external_id,
                created_at = rec.created_at,
                currency = rec.currency_iso3,
                currency_amount = dec_str(rec.currency_amount),
                btc_rate = dec_str(rec.btc_rate),
                btc_amount = dec_str(rec.btc_amount)
            ) 
            for rec in db_page
        ],
        last_reference = str(db_page[-1].external_id) if db_page else None
    )