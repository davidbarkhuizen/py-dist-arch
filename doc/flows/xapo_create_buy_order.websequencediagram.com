title create buy order

actor client

participant create_buy_order
participant btc_price
participant write_model
participant sync_q
participant read_model_sync
participant read_model
participant coinbase

client -> create_buy_order: PUT \n http://localhost:8777/buy_order \n CreateBuyOrderRequest \n { currency, amount, idempotence_key }
create_buy_order -> btc_price: GET \n /buy
btc_price -> coinbase: GET \n api.coinbase.com/v2/prices/buy?currency=XXX
coinbase -> btc_price: btc_rate
btc_price -> create_buy_order: btc_rate\n INSERT buy_order
create_buy_order -> write_model: INSERT \n 1. buy_order \n 2. buy_order_idempotence_cache \n (key, currency, amount, client_id)
alt idempotence_cache inserts succeed => cache miss
    create_buy_order->sync_q: buy_order_dto
elseidempotence_cache inserts fail => cache hit
    create_buy_order -> write_model: SELECT buy_order_idempotence_cache \n (key, currency, amount, client_id)
    write_model -> create_buy_order: buy_order_id
    create_buy_order -> write_model: SELECT buy_order
    write_model -> create_buy_order: buy_order
end
create_buy_order -> client: CreateBuyOrderResponse \n { idempotence_key, buy_order }

sync_q -> read_model_sync: buy_order_dto
read_model_sync -> read_model: INSERT \n buy_order_read_model