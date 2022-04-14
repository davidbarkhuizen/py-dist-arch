from typing import Optional

from sqlalchemy.engine.base import Engine
from util.service_base import ServiceDefinition, serve
from services.migration.client import MigrationServiceClient
from util.env import database_endpoint_from_env, endpoint_from_env

from model.common import DatabaseEndPoint, Endpoint, Service
from util.db import get_tested_database_engine
from services.fetch_buy_orders.service import api, configure_api

def service_definition():

    read_model_db_endpoint: Optional[DatabaseEndPoint] = None
    migration_endpoint: Optional[Endpoint] = None
    migration_client = None
    read_model_engine: Optional[Engine] = None

    def configure_service():
        nonlocal read_model_db_endpoint, migration_endpoint, migration_client, read_model_engine

        migration_endpoint = endpoint_from_env('MIGRATION', no_path = True)
        migration_client = MigrationServiceClient(migration_endpoint)
        migration_client.wait_for_migrations()

        read_model_db_endpoint = database_endpoint_from_env('READ_MODEL_DB')        
        read_model_engine = get_tested_database_engine(read_model_db_endpoint)
        
        configure_api(read_model_engine)        

    return ServiceDefinition(Service.FETCH_BUY_ORDERS, configure_service, None, api)

serve(service_definition())