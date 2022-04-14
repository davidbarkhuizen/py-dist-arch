from model.orm.read_model import BuyOrderReadModel
from sqlalchemy.orm import Session
from util.db import get_tested_database_engine
from services.migration.client import MigrationServiceClient
from typing import Callable, Optional
from model.common import DatabaseEndPoint, Endpoint, QueueEndpoint
from util.service_base import ServiceDefinition, serve
from util.queue import connect_blocking_q_listener
from util.env import database_endpoint_from_env, endpoint_from_env, queue_endpoint_from_env
from model.common import Queue, Service
import traceback
from util.events import log_event
from model.logevent import BuyOrderReadModelSynced, FailedToSyncBuyOrderReadModel
from model.dto import BuyOrderDTO

def service_definition():

    q_ep: Optional[QueueEndpoint] = None
    
    read_model_db_endpoint: Optional[DatabaseEndPoint] = None
    read_model_engine: Optional[Callable] = None

    migration_endpoint: Optional[Endpoint] = None
    migration_client: Optional[Callable] = None

    def configure_service():
        nonlocal q_ep, read_model_db_endpoint, migration_endpoint, migration_client, read_model_engine

        read_model_db_endpoint = database_endpoint_from_env('READ_MODEL_DB')        
        read_model_engine = get_tested_database_engine(read_model_db_endpoint)

        migration_endpoint = endpoint_from_env('MIGRATION', no_path = True)
        migration_client = MigrationServiceClient(migration_endpoint)
        migration_client.wait_for_migrations()

        q_ep = queue_endpoint_from_env('Q', Queue.BuyOrder)

    def sync_buy_order(model_dict: str, ack):
        try:
            dto = BuyOrderDTO.parse_obj(model_dict)            
            
            read_model: Optional[BuyOrderReadModel] = None

            with Session(read_model_engine) as db_session:
                with db_session.begin():            
                    read_model = BuyOrderReadModel(
                        id = dto.id,
                        created_at = dto.created_at, 
                        external_id = dto.external_id,

                        client_id = dto.client_id,

                        currency_id = dto.currency_id,
                        currency_iso3 = dto.currency_iso3,
                        
                        currency_amount = dto.currency_amount,
                        btc_rate = dto.btc_rate,
                        btc_amount = dto.btc_amount
                    )
                    db_session.add(read_model)            

                    log_event(BuyOrderReadModelSynced(id=dto.id))
                    ack()

        except:
            log_event(
                FailedToSyncBuyOrderReadModel(
                    id=dto.id,
                    info=traceback.format_exc()
                )
            )

    def run_logic():
        connect_blocking_q_listener(q_ep, sync_buy_order)

    return ServiceDefinition(Service.READ_MODEL_SYNC, configure_service, run_logic, None)

serve(service_definition())