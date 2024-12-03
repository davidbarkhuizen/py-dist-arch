# BUILD_OPTIONS="--no-cache"
BUILD_OPTIONS=""
ROOT="docker/services"

docker build -t write_model:latest -f $ROOT/database/write_model/Dockerfile .
docker build -t read_model:latest -f $ROOT/database/read_model/Dockerfile .
docker build -t log:latest -f $ROOT/log/Dockerfile .

docker build -t create_buy_order:latest -f $ROOT/create_buy_order/Dockerfile $BUILD_OPTIONS .
docker build -t fetch_buy_orders:latest -f $ROOT/fetch_buy_orders/Dockerfile $BUILD_OPTIONS .
docker build -t queue:latest -f $ROOT/queue/Dockerfile $BUILD_OPTIONS .
docker build -t read_model_sync:latest -f $ROOT/read_model_sync/Dockerfile $BUILD_OPTIONS .
docker build -t migration:latest -f $ROOT/migration/Dockerfile $BUILD_OPTIONS .
docker build -t btc_price:latest -f $ROOT/btc_price/Dockerfile $BUILD_OPTIONS .