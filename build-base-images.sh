# BUILD_OPTIONS="--no-cache"
BUILD_OPTIONS=""
ROOT="docker/services"

docker build -t common-python-base:latest -f $ROOT/common/Dockerfile.base $BUILD_OPTIONS .

docker build -t db-base:latest -f $ROOT/database/Dockerfile.base $BUILD_OPTIONS .
docker build -t log-base:latest -f $ROOT/log/Dockerfile.base $BUILD_OPTIONS .
docker build -t queue-base:latest -f $ROOT/queue/Dockerfile.base $BUILD_OPTIONS .

docker build -t read-model-sync-base:latest -f $ROOT/read_model_sync/Dockerfile.base $BUILD_OPTIONS .
docker build -t migration-base:latest -f $ROOT/migration/Dockerfile.base $BUILD_OPTIONS  .
docker build -t btc-price-base:latest -f $ROOT/btc_price/Dockerfile.base $BUILD_OPTIONS  .
docker build -t create-buy-order-base:latest -f $ROOT/create_buy_order/Dockerfile.base $BUILD_OPTIONS .
docker build -t fetch-buy-orders-base:latest -f $ROOT/fetch_buy_orders/Dockerfile.base $BUILD_OPTIONS .