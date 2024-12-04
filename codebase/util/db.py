import traceback
from typing import Optional
from model.common import DatabaseEndPoint
import time

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import text

from util.events import log_event
from model.logevent import ConnectedToDatabase, FailedToConnectToDatabase

def connection_string(port, host, database, user, password):
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

def define_engine(ep: DatabaseEndPoint):
    return create_engine(connection_string(ep.port, ep.host, ep.database, ep.user, ep.pwd))

def get_tested_database_engine(ep: DatabaseEndPoint):
    '''no retry if (retry_wait_s == 0)'''

    engine = define_engine(ep)

    connected_db_name: Optional[str] = None
    while not connected_db_name:
        try:
            with engine.connect() as connection:

                values = connection.execute(text('SELECT current_database();'))    
                connected_db_name, = values.all()[0]
                connection.close()
            
        except:
            log_event(
                FailedToConnectToDatabase(
                    database=ep.database,
                    port=str(ep.port),
                    host=ep.host,
                    user=ep.user,
                    error=traceback.format_exc()
                )
            )
            
            if ep.retry_wait_s == 0:
                raise

            time.sleep(float(ep.retry_wait_s))
            continue

    log_event(
        ConnectedToDatabase(
            database=connected_db_name,
            port=ep.port,
            host=ep.host,
            user=ep.user
        )
    )
    
    return engine