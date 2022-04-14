from util.env import env_str
from model.common import DatabaseEndPoint, Endpoint

def url(protocol:str, host:str, port:str, path:str=None):
    root = f'{protocol}://{host}:{port}'
    return root if not path else f'{root}{path}'

def url_for_endpoint(ep: Endpoint):
    return url(ep.protocol, ep.host, ep.port, ep.path)