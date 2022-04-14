from model.common import DatabaseEndPoint, Endpoint, QueueEndpoint, Queue
import os

def env_str(key: str):
    return os.environ[key]

def env_int(key: str):
    return int(os.environ[key])

def env_float(key: str):
    return float(env_str(key))

def database_endpoint_from_env(prefix: str):
    prefix = prefix.upper()
    return DatabaseEndPoint(
        protocol='http',
        host=env_str(f'{prefix}_HOST'),
        port=env_int(f'{prefix}_PORT'),
        database=env_str(f'{prefix}_NAME'),
        user=env_str(f'{prefix}_USER'),
        pwd=env_str(f'{prefix}_PWD'),
        retry_wait_s=env_int(f'{prefix}_RETRY_WAIT_S')
    )

def endpoint_from_env(prefix: str, no_path: bool = False):
    prefix = prefix.upper()
    return Endpoint(
        protocol=env_str(f'{prefix}_PROTOCOL'),
        host=env_str(f'{prefix}_HOST'),
        port=env_int(f'{prefix}_PORT'),
        path=env_str(f'{prefix}_PATH') if not no_path else None
    )

def queue_endpoint_from_env(prefix: str, queue: Queue):
    prefix = prefix.upper()
    return QueueEndpoint(
        host=env_str(f'{prefix}_HOST'),
        port=env_int(f'{prefix}_PORT'),
        exchange=env_str(f'{prefix}_EXCHANGE'),
        queue=queue
    )