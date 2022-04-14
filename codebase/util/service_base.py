import sys, traceback
from typing import Callable, Optional
from dataclasses import dataclass

from fastapi.applications import FastAPI
import uvicorn

from util.events import configure_and_wait_for_logging
from model.logevent import ServiceConfigurationExceptionOccurred, ServiceRunLogicExceptionOccurred, ServiceShutDown, ServiceWebServeExceptionOccurred
from model.common import Service
from util.events import log_event
from util.env import env_int, env_str

from dataclasses import dataclass

@dataclass
class ServiceDefinition:
    service: Service
    configure_service: Callable
    run_logic: Callable
    web_api: FastAPI

def serve(service: ServiceDefinition):

    configure_and_wait_for_logging(service.service)

    try:

        host: Optional[str] = None
        port: Optional[int] = None

        try:
            host=env_str('SERVICE_HOST')
            port=env_int('SERVICE_PORT')

            if service.configure_service:
                service.configure_service()

        except:
            log_event(ServiceConfigurationExceptionOccurred(info=traceback.format_exc()))
            raise

        try:
            if service.run_logic:
                service.run_logic()
        except:
            log_event(ServiceRunLogicExceptionOccurred(info=traceback.format_exc()))
            raise

        try:
            if service.web_api:
                uvicorn.run(
                    service.web_api, 
                    host=host, 
                    port=port, 
                    log_level="info"
                )
        except:
            log_event(ServiceWebServeExceptionOccurred(info=traceback.format_exc()))
            raise

        log_event(ServiceShutDown(exit_code = 0))
        sys.exit(0)

    except:
        log_event(ServiceShutDown(exit_code = 1))
        sys.exit(1)