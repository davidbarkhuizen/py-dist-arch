import time
from typing import Optional
from util.env import env_float
import os, traceback
from fluent import sender, event
from model.logevent import LoggingTag
from model.common import Service
from pydantic.main import BaseModel
import inflection

class ExceptionOccurred(BaseModel):
    _tag = 'exception_occurred'
    msg: str
    stack_trace: Optional[str] = ...

class ConnectedToLogging(BaseModel):
    _tag = 'logging_connected'

class FailedToConnectToLogging(BaseModel):
    _tag = 'failed_to_connect_to_logging'
    host: str
    port: str
    info: str

def log_event(event_model: BaseModel):
    tag = inflection.underscore(type(event_model).__name__)
    event.Event(tag, event_model.dict())

def log_exception(msg):
    log_event(ExceptionOccurred(msg=msg, stack_trace=traceback.format_exc()))

def configure_and_wait_for_logging(service: Service):

    try:
        host = os.environ['LOGGING_HOST']
        port = int(os.environ['LOGGING_PORT'])
        sender.setup(f'{LoggingTag.Root.value}.{service.value}', host=host, port=port)
    except:
        print(f'error configuring logging for {service.value} @ {host} {port}: {traceback.format_exc()}')
        raise

    retry_s = env_float('LOGGING_RETRY_S')
    
    while True:
        try:
            log_event(ConnectedToLogging())
            break
        except:
            log_event(FailedToConnectToLogging(host=host, port=port, info=traceback.format_exc()))
            time.sleep(retry_s)