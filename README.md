# distributed python architecture

david.barkhuizen@gmail.com, 2021/09/02

## Important Note on Authentication, Security & Data Persistence

This demonstration system features no authentication, has not been secured, and is not intended for production use.  Furthermore, no guarantees are made as no data persistence.  While reasonable efforts have been mad eto source components from reputable sources, you use this system entirely at your own risk, and the author accepts no responsibility whatsoever for its use or misuse.

## Setup & Installation

### Pre-Requisites

docker, docker-compose, curl, python(3)

### Build

#### External Docker Base Images

Note:  Where-ever possible Alpine linux based images have been used.

image|technology|services
-----|----------|--------
postgres:13.4-alpine|postgres database|read_model, write_model
fluent/fluentd:v1.13.0-1.0|fluentd event logger|log
rabbitmq:3.9-management-alpine|rabbitmq queue|queue
tiangolo/uvicorn-gunicorn:python3.8-alpine3.10|python fastapi|btc_price, create_buy_order, fetch_buy_orders, migration, read_model_sync

#### Build Script Sequence

1. ```./build_base_images.sh```  
2. ```./build_run_images.sh```  

### Run

#### Run Script

```./run.sh```

#### Docker-Compose Services

service|function
-------|--------
log|fluentd event log
write_model|write data model
read_model|read data model
migration|database migration
queue|event queues - buy order read model sync
read_model_sync|sync read model from queue
btc_price|fetch btc price from external api.coinbase.com
create_buy_order|expose create buy order @ PUT http://localhost:8777/buy_order
fetch_buy_orders|expose fetch buy orders @ GET http://localhost:8778/buy_orders

### Monitoring

- the services emit numerous structured logging events to facilitate operation and fault finding
- these events are 

### Test

#### Automated Python Unit Tests

```./test.sh```

#### Manual Curl Tests Scripts

1. create buy order  
```.../xapo/curl$ ./put_buy_order.sh```  

Note:  the combination of (idempotence_key, currency, amount) must be unique  

2. get buy order - first page  
```.../xapo/curl$ ./get_buy_order.sh```  

3. get buy order - get subsequent pages  
```.../xapo/curl$ ./get_buy_orders_pass_last_ref.sh```  

Note:  `last_reference`  
- refers to the id of the last row on the previous page  
- is explictly returned for each page, for use in retrieving the next page