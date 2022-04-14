# from model.common import SUPPORTED_CURRENCIES
# from util.web import endpoint_from_env, url_for_endpoint
# from test.utils.util import ok
# import unittest
# import requests

# price_ep = endpoint_from_env('price')
# price_url = url_for_endpoint(price_ep)

# class TestPriceService(unittest.TestCase):

#     def __init__(self, *args, **kwargs):
#         super(TestPriceService, self).__init__(*args, **kwargs)

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def test_that_price_quotes_in_all_supported_currencies_are_returned(self):                
#         for currency in SUPPORTED_CURRENCIES:        
#             order = { 'currency': currency, 'amount': 1 }
#             rsp = requests.put(price_url, json=order)        
#             self.assertTrue(ok(rsp))