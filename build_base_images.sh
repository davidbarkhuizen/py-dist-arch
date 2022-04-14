docker build -t db_base:001 -f docker/services/database/Dockerfile.base --no-cache .
docker build -t log_base:001 -f docker/services/log/Dockerfile.base --no-cache .
docker build -t queue_base:001 -f docker/services/queue/Dockerfile.base --no-cache .
docker build -t read_model_sync_base:001 -f docker/services/read_model_sync/Dockerfile.base --no-cache .
docker build -t migration_base:001 -f docker/services/migration/Dockerfile.base --no-cache  .
docker build -t btc_price_base:001 -f docker/services/btc_price/Dockerfile.base --no-cache  .
docker build -t create_buy_order_base:001 -f docker/services/create_buy_order/Dockerfile.base --no-cache .
docker build -t fetch_buy_orders_base:001 -f docker/services/fetch_buy_orders/Dockerfile.base --no-cache .