from fastapi.exceptions import HTTPException
import traceback
import uuid
from model.logevent import RequestFailed
from typing import Callable
from util.events import log_event

def request_handler(request_name: str, log_event_model: Callable, callback: Callable):
    
    def handle(*args):
        
        # NEXT determine client_id from stateless header-sourced authentication token
        client_id: int = 1        

        try:
            log_event(log_event_model(client_id, *args))
            rsp = callback(client_id, *args)
            return rsp
        except:
            error_reference = uuid.uuid4()
            log_event( 
                RequestFailed(
                    request=request_name,
                    error=traceback.format_exc(),
                    reference=str(error_reference)
                )
            )
            raise HTTPException(
                status_code=500, 
                detail=f'an error occurred.  please contact xapo support and quote reference {error_reference}'
            )
    
    return handle