import uuid
import unittest

from services.create_buy_order.rqrsp import CreateBuyOrderResponse
from model.common import MAX_BUY_ORDER_SIZE_EXCLUSIVE_ANY_CURRENCY_UNIT, SUPPORTED_CURRENCIES, Currency
from test.utils import put_buy_order, create_buy_order_request, is_200, random_string_not_in

class TestCreateBuyOrderService(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCreateBuyOrderService, self).__init__(*args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_supported_currencies_are_accepted(self):                
        for currency in SUPPORTED_CURRENCIES:     
            rsp = put_buy_order(currency, '100.00', uuid.uuid4())   
            self.assertEqual(rsp.status_code, 200)

    def test_random_non_supported_currency_are_rejected(self):        
        currency = random_string_not_in(3, SUPPORTED_CURRENCIES).upper()
        rsp = put_buy_order(currency, '100.00', uuid.uuid4())   
        self.assertIn(rsp.status_code, [400, 422])
 
    def test_negative_amounts_are_rejected(self):
        rsp = put_buy_order(Currency.USD.value, '-1.00', uuid.uuid4())   
        self.assertIn(rsp.status_code, [400, 422])

    def test_zero_amounts_are_rejected(self):
        rsp = put_buy_order(Currency.USD.value, '0', uuid.uuid4())   
        self.assertIn(rsp.status_code, [400, 422])

    def test_order_amount_exceeding_the_max_is_rejected(self):
        rsp = put_buy_order(Currency.USD.value, str(MAX_BUY_ORDER_SIZE_EXCLUSIVE_ANY_CURRENCY_UNIT))        
        self.assertIn(rsp.status_code, [400, 422])

    # def test_light_load(self):
    #     for i in range(100):        
    #         rsp = put_buy_order(Currency.USD.value, '0.01', uuid.uuid4())   
    #         self.assertIn(rsp.status_code, [200])

    def test_request_without_idempotence_key_fails(self):
        rsp = put_buy_order(Currency.USD.value, '0.01', None)
        self.assertIn(rsp.status_code, [422])

    def test_resending_identical_request_returns_same_response(self):
        idempotence_key = str(uuid.uuid4())
        rsp_1 = CreateBuyOrderResponse.parse_raw(put_buy_order(Currency.USD.value, '0.01', idempotence_key).text)
        rsp_2 = CreateBuyOrderResponse.parse_raw(put_buy_order(Currency.USD.value, '0.01', idempotence_key).text)
        self.assertEqual(rsp_1.buy_order.id, rsp_2.buy_order.id)
        self.assertEqual(rsp_1, rsp_2)

    # def test_05_a_successful_order_is_persisted(self):
    #     raise NotImplementedError()

    # def test_06_persisted_order_info_is_correct(self):
    #     # - id, amount, currency, exchange rate, bitcoin amount
    #     raise NotImplementedError()

    # def test_08_the_sum_of_btc_across_all_buy_orders_doesnt_exceed_threshold(self):
    #     raise NotImplementedError()

    # 4. confirm bitcoin precision at 8 decimal digits
    # 4. confirm that rounding is up
    # 5. confirm that precision is not lost in calculation
    
    # read model / get service
    # - an order can be retrieved (i.e. a successful order is persisted in the read model, and can be retrieved)

if __name__ == '__main__':
    unittest.main()