from decimal import Decimal, getcontext, ROUND_UP

def configure_decimal_context():
    getcontext().prec = 8
    getcontext().rounding = ROUND_UP

def calc_btc_amt_from_ccy_amount_and_btc_rate(ccy_amount: Decimal, btc_rate: Decimal):
    return ccy_amount / btc_rate

def dec_str(d: Decimal):
    return '{0:f}'.format(d)