from typing import Callable, List, Optional
from sqlalchemy.sql.expression import select
from services.btc_price.client import BtcPriceServiceClient
from decimal import Decimal
import traceback
from sqlalchemy.engine.base import Engine

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from model.dto import BuyOrderDTO
from util.calc import calc_btc_amt_from_ccy_amount_and_btc_rate, configure_decimal_context, dec_str
from util.events import log_event
from services.create_buy_order.rqrsp import BuyOrderExport, CreateBuyOrderRequest, CreateBuyOrderResponse
from model.orm.write_model import BuyOrder, BuyOrderIdempotenceCache, Currency
from model.logevent import BtcPriceClientFailed, BuyOrderCreated, BuyOrderRequestIdempotenceCacheHit, CreateBuyOrderRequestReceived, CreateBuyOrderResponseReturned, ErrorRetrievingBuyOrderRequestViaIdempotenceCache, ModelUpdateFailed

write_engine: Optional[Engine] = None
q_publisher: Optional[Callable] = None
btc_price_service: Optional[BtcPriceServiceClient] = None
currencies: List[Currency] = None

def configure_logic(write_engine_: Engine, q_publisher_, btc_price_service_: BtcPriceServiceClient):
    global write_engine, q_publisher, btc_price_service, currencies
    
    write_engine = write_engine_

    with Session(write_engine) as db_session:
        stmt = select(Currency)
        currencies = db_session.execute(stmt).scalars().all()

    q_publisher = q_publisher_
    btc_price_service = btc_price_service_

    configure_decimal_context()

def handle_create_buy_order_request(client_id: int, rq: CreateBuyOrderRequest):

    write_model: Optional[BuyOrder] = None
    currency = [ccy for ccy in currencies if ccy.iso3 == rq.currency][0]

    ccy_per_unit_btc = btc_price_service.get_buy_price(rq.currency)
    if not ccy_per_unit_btc:            
        btc_price_client_failed = BtcPriceClientFailed(currency = rq.currency)
        log_event(btc_price_client_failed)
        raise Exception(btc_price_client_failed.json())

    ccy_amount_decimal = Decimal(rq.amount)
    ccy_per_unit_btc_decimal = Decimal(ccy_per_unit_btc)
    btc_amount_decimal = calc_btc_amt_from_ccy_amount_and_btc_rate(ccy_amount_decimal, ccy_per_unit_btc_decimal)

    is_idempotent: bool = False
    try:
        with Session(write_engine) as db_session:

            with db_session.begin():            

                write_model = BuyOrder(
                    client_id = client_id,
                    currency_id = currency.id,
                    currency_amount = ccy_amount_decimal,
                    btc_rate = ccy_per_unit_btc_decimal,
                    btc_amount = btc_amount_decimal
                )
                db_session.add(write_model)
                db_session.flush()

                try:
                    idempotence_check = BuyOrderIdempotenceCache(
                        client_id = client_id,
                        currency_id = currency.id,
                        currency_amount = ccy_amount_decimal,                            
                        idempotence_key = rq.idempotence_key,
                        buy_order_id = write_model.id
                    )
                    db_session.add(idempotence_check)
                    db_session.flush()
                except IntegrityError:
                    log_event(
                        BuyOrderRequestIdempotenceCacheHit(
                            client_id = client_id,
                            currency = rq.currency,
                            amount = str(rq.amount),
                            idempotence_key = str(rq.idempotence_key)                                
                        )
                    )                       
                    is_idempotent = True
                    raise

                q_publisher(
                    BuyOrderDTO(
                        id = write_model.id,
                        client_id = write_model.client_id,
                        external_id = write_model.external_id,
                        created_at = write_model.created_at,                            

                        currency_iso3 = currency.iso3,
                        currency_id = write_model.currency_id,
                        currency_amount = write_model.currency_amount,
                        btc_rate = write_model.btc_rate,
                        btc_amount = write_model.btc_amount                 
                    )
                )

            log_event(
                BuyOrderCreated(
                    id=write_model.id, 
                    external_id=str(write_model.external_id)
                )
            )
            log_event(
                CreateBuyOrderResponseReturned(
                    external_id=str(write_model.external_id)
                )
            )

            return CreateBuyOrderResponse(
                idempotence_key = rq.idempotence_key,
                buy_order = BuyOrderExport(
                    id = str(write_model.external_id),
                    created_at = write_model.created_at,
                    currency = rq.currency,
                    currency_amount = dec_str(write_model.currency_amount),
                    btc_rate = dec_str(write_model.btc_rate),
                    btc_amount = dec_str(write_model.btc_amount),                    
                )
            )
    except:
        if not is_idempotent:
            log_event(
                ModelUpdateFailed(
                    model='BuyOrder',
                    info=traceback.format_exc()                    
                )
            )
            raise

    if is_idempotent:
        try:
            with Session(write_engine) as db_session:

                idempotence_match = db_session.query(BuyOrderIdempotenceCache)\
                    .filter(
                        BuyOrderIdempotenceCache.client_id == client_id,
                        BuyOrderIdempotenceCache.currency_id == currency.id,
                        BuyOrderIdempotenceCache.currency_amount == ccy_amount_decimal,
                        BuyOrderIdempotenceCache.idempotence_key == rq.idempotence_key
                    ).one()

                write_model_match = db_session.query(BuyOrder)\
                    .filter(BuyOrder.id == idempotence_match.buy_order_id).one()

                return CreateBuyOrderResponse(
                    idempotence_key = rq.idempotence_key,
                    buy_order = BuyOrderExport(
                        id = str(write_model_match.external_id),
                        created_at = write_model_match.created_at,
                        currency = rq.currency,
                        currency_amount = dec_str(write_model_match.currency_amount),
                        btc_rate = dec_str(write_model_match.btc_rate),
                        btc_amount = dec_str(write_model_match.btc_amount)
                    )
                )

        except:
            log_event(
                ErrorRetrievingBuyOrderRequestViaIdempotenceCache(
                    client_id = client_id,
                    currency = rq.currency,
                    amount = rq.amount,
                    idempotence_key = rq.idempotence_key,
                    info = traceback.format_exc()
                )
            )
            raise

def rq_received_logevent(client_id, rq):
    return CreateBuyOrderRequestReceived(
        currency=rq.currency, 
        amount=rq.amount,
        idempotence_key=str(rq.idempotence_key),
        client_id=client_id
    )