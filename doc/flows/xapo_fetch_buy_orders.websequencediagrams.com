title fetch buy orders

actor client

participant fetch_buy_orders
participant read_model

client -> fetch_buy_orders: GET \n http://locahost:8778 \n /buy_orders \n ?last_reference&page_size
fetch_buy_orders -> read_model: SELECT buy_order_read_model \n(keyset paged)
read_model -> fetch_buy_orders: buy_order_read_model_page
fetch_buy_orders -> client: BuyOrderPage \n { rows, last_reference }