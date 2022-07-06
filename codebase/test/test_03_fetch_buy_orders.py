from services.fetch_buy_orders.rqrsp import BuyOrderPage
from util.web import url_for_endpoint
import unittest
import requests

from test.utils import is_200, random_string_not_in
from util.env import endpoint_from_env

fetch_buy_orders_ep = endpoint_from_env('fetch_buy_orders')
fetch_buy_orders_url = url_for_endpoint(fetch_buy_orders_ep)

buyorder_ep = endpoint_from_env('create_buy_order')
buyorder_url = url_for_endpoint(buyorder_ep)

class TestFetchBuyOrderService(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFetchBuyOrderService, self).__init__(*args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_request_with_no_parameters(self):                
        rsp = requests.get(fetch_buy_orders_url)   
        self.assertEqual(rsp.status_code, 200)

    def test_non_default_page_size(self):                
        non_default_page_size = 19
        rsp = requests.get(fetch_buy_orders_url, params={'page_size': non_default_page_size})   
        self.assertEqual(rsp.status_code, 200)
        
        page = BuyOrderPage.parse_raw(rsp.text)
        self.assertEqual(len(page.rows), non_default_page_size)