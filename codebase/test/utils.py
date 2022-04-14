import random, string, uuid
import requests
from util.web import url_for_endpoint
from util.env import endpoint_from_env

buyorder_ep = endpoint_from_env('create_buy_order')
buyorder_url = url_for_endpoint(buyorder_ep)

def create_buy_order_request(currency: str, amount: str, idempotence_key: uuid.UUID):
    return {
        'currency':currency,
        'amount':amount,
        'idempotence_key': str(idempotence_key)
    } 

def put_buy_order(currency: str, amount: str, idempotence_key: uuid.UUID = None):
    rsp = requests.put(buyorder_url, json=create_buy_order_request(currency, amount, idempotence_key))   
    return rsp

def random_string(length: int, letters = string.ascii_lowercase):
    return ''.join(random.choice(letters) for i in range(length))

def random_string_not_in(length: int, not_in, letters = string.ascii_lowercase):
    
    def rnd():
        return random_string(length, letters)

    candidate = rnd()
    while candidate in not_in:    
        candidate = rnd()

    return candidate

def is_200(rsp):
    return rsp.status_code == 200

def is_4xx(rsp):
    return str(rsp.status_code).startswith('4')

def is_400(rsp):
    return rsp.status_code == 400

def is_422(rsp):
    return rsp.status_code == 422


def print_response_info(rsp):    
    print(rsp.status_code, rsp.reason, rsp.text)     