from typing import Optional
from util.service_base import ServiceDefinition, serve
import traceback, sys

from yoyo import read_migrations, get_backend

from util.env import database_endpoint_from_env
from util.db import get_tested_database_engine
from util.events import log_event
from model.logevent import DatabaseMigrated, DatabaseMigrationExceptionOccurred
from model.common import DatabaseEndPoint, Endpoint
from services.migration.service import api
from model.common import Service

def migrate(ep: DatabaseEndPoint, relative_folder_path: str):
    try:
        backend = get_backend(f'postgresql://{ep.user}:{ep.pwd}@{ep.host}:{ep.port}/{ep.database}')
        migrations = read_migrations(relative_folder_path)
        backend.apply_migrations(backend.to_apply(migrations))
        log_event(DatabaseMigrated(database=ep.database))
    except Exception:
        log_event(DatabaseMigrationExceptionOccurred(database=ep.database, info=traceback.format_exc()))
        raise

def service_definition():

    write_model_db_endpoint: Optional[Endpoint] = None
    read_model_db_endpoint: Optional[Endpoint] = None

    def configure_service():
        nonlocal write_model_db_endpoint, read_model_db_endpoint

        write_model_db_endpoint = database_endpoint_from_env('WRITE_MODEL_DB')
        get_tested_database_engine(write_model_db_endpoint)    

        read_model_db_endpoint = database_endpoint_from_env('READ_MODEL_DB')
        get_tested_database_engine(read_model_db_endpoint)

    def run_logic():
        migrate(write_model_db_endpoint, 'model/migrations/write_model')       
        migrate(read_model_db_endpoint, 'model/migrations/read_model')

    return ServiceDefinition(Service.MIGRATION, configure_service, run_logic, api)

serve(service_definition())