# Xapo Technical Assigment Specification

## Task

1) Create a REST API according to the functional requirements.
2) Use a programming language and relational database of your choice.
3) Responses should be all in JSON.
4) Provide an automated test suite for the app.
5) Use CoinDesk Bitcoin price API to source exchange rates.
Please refer to the documentation at https://www.coindesk.com/coindesk-api
6) The final API will be tested using CURL, so you will need to include a read.me file in your project's root folder with examples of curls for testing and how to start your API.
7) Wrap up everything in Docker. Use several containers. Put them together using Docker compose.
8) Follow the Twelve-Factor App methodology

## Functional requirements:

API allows its clients to manage BTC buy orders. Clients place orders to purchase BTC for fiat at a market price. API does not create transactions on the Bitcoin blockchain, but simply stores the order information in its database for further processing.

1) Create Buy Order

a. Creation of a Buy Order requires the following data at minimum:

* currency - represents the currency (ISO3 code one of: EUR, GBP, USD)
* amount - represents the amount of currency (0 < x < 1,000,000,000)

You can introduce additional data if that helps to fulfill the requirements.

b. Successful call should store the order in the database. The following info should be
stored at a minimum:

* id - order's unique identifier
* amount - requested fiat amount
* currency - requested fiat currency
* exchange rate - value of BTC versus the requested fiat; BTC is the base currency and requested fiat is the quote currency; use the third-party API to source the exchange rates
* bitcoin amount - amount of BTC which the requested amount of fiat buys at the exchange rate. Use a precision of 8 decimal digits, and always round up. Do not lose precision in calculations

c. Buy Order creation must be idempotent.

d. Sum of bitcoin amount of all orders stored in the system must not exceed 100BTC.

System must not allow creation of new orders which would cause the constraint to be violated.

2) Fetch Buy Order collection

Returns Buy Orders stored in the database in reverse chronological order.

Resources must have the following attributes at minimum: id, amount, currency, exchange rate, bitcoin amount. Responses must be paged. Response time should be the same regardless which page is requested.

You can introduce additional data if that helps to fulfill the requirements.

## Coinbase API

e.g. curl https://api.coinbase.com/v2/prices/spot?currency=USD

### USD

{"data":{"base":"BTC","currency":"USD","amount":"48478.88"}}

### GBP

{"data":{"base":"BTC","currency":"GBP","amount":"35330.89"}}

### EUR

{"data":{"base":"BTC","currency":"EUR","amount":"41191.91"}}

### JPY

{"data":{"base":"BTC","currency":"JPY","amount":"5333330.8622"}}

### VND

{"data":{"base":"BTC","currency":"VND","amount":"1102629650.42667017"}}