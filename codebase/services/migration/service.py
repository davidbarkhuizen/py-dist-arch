from fastapi import FastAPI

from model.logevent import HealthChecked
from util.events import log_event

api = FastAPI()

@api.get("/healthcheck")
async def get_healtcheck():
    log_event(HealthChecked())