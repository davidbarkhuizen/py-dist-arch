docker build -t write_model:001 -f docker/services/database/write_model/Dockerfile .
docker build -t read_model:001 -f docker/services/database/read_model/Dockerfile .
docker build -t log:001 -f docker/services/log/Dockerfile .
docker build -t create_buy_order:001 -f docker/services/create_buy_order/Dockerfile --no-cache .
docker build -t fetch_buy_orders:001 -f docker/services/fetch_buy_orders/Dockerfile --no-cache .
docker build -t queue:001 -f docker/services/queue/Dockerfile --no-cache .
docker build -t read_model_sync:001 -f docker/services/read_model_sync/Dockerfile --no-cache .
docker build -t migration:001 -f docker/services/migration/Dockerfile --no-cache .
docker build -t btc_price:001 -f docker/services/btc_price/Dockerfile --no-cache .