import traceback
from util.web import url_for_endpoint
import time
from model.logevent import MigrationsServiceConnectionError, WaitingForMigrations
from util.events import log_event
from model.common import Endpoint
import requests
from util.web import url_for_endpoint

class MigrationServiceClient:
    
    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint
        self.endpoint.path = '/healthcheck'

    def is_migrated(self):
        try:      
            url = url_for_endpoint(self.endpoint)
            status_code = requests.get(url).status_code
            return status_code == 200
        except:
            log_event(MigrationsServiceConnectionError(error_text=traceback.format_exc()))
            return False

    def wait_for_migrations(self):

        while True:
            if self.is_migrated():
                break

            log_event(WaitingForMigrations())
            time.sleep(float(self.endpoint.retry_wait_s))