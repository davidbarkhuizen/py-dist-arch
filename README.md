# distributed python architecture

david.barkhuizen@gmail.com, 2021/09/02

## Important Note on Authentication, Security & Data Persistence

This demonstration system features no authentication, has not been secured, and is not intended for production use.  Furthermore, no guarantees are made as no data persistence.  While reasonable efforts have been mad eto source components from reputable sources, you use this system entirely at your own risk, and the author accepts no responsibility whatsoever for its use or misuse.

## Architecture

This POC is is intended to fulfill the functional requirements listed in `docs/specifiction.md`, using the 12 factor app methodology as summarised in `docs/12_factors.md`, and implemented as a containerised solution.  

### Component Technologies

|aspect|technology|
|------|----------|
|Database|Postgres|
|ORM|SqlAlchemy|
|Models|Pydantic|
|REST server|FastAPI|
|Queue|RabbitMQ|
|Structured Event Logging|FluentD|

### Write/Read Model

The architecture splits the data persistence into a write model and a read model.  The write model is intended as the golden source of truth.  The read model is kept in sync with the write model using an event service (queue).  This allows the write model table structures to be optimized for fast insert and update, whereas by contrast the read model table structures are optimized for fast read.

#### Create Request Idempotence

A specific requirement was around idempotence of create requests, and there is some complication in the database structure which supports this.  

## Setup & Installation

### Host Machine Pre-Requisites

1. Docker, Docker-Compose
2. curl
3. python3  
4. pydantic pip3 module `sudo pip3 install pydantic`

### Build

#### External Docker Base Images

Note:  Where-ever possible Alpine linux based images have been used to reduce image size and reduce attack surface.  

image|technology|services
-----|----------|--------
postgres:13.4-alpine|postgres database|read_model, write_model
fluent/fluentd:v1.13.0-1.0|fluentd event logger|log
rabbitmq:3.9-management-alpine|rabbitmq queue|queue
tiangolo/uvicorn-gunicorn:python3.8-alpine3.10|python fastapi|btc_price, create_buy_order, fetch_buy_orders, migration, read_model_sync

#### Build Script Sequence

Assuming that docker-compose is running on the host machine, execute the following shell scripts from the repo root:  

1. ```./build_base_images.sh```  
2. ```./build_run_images.sh```  

### Run

#### Run Script

Execute the following shell script to launch the cluster.  

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
- these events are emitted to fluentd  

### Test

#### Pre-Requisites

##### pydantic

The test shell script `./test.sh` assumes that the python module `pydantic` has been installed on the host machine.  

The quick and dirty way to do this is a raw (no-venv) global pip3 install:  

    $ pip3 install pydantic

#### Automated Python Unit Tests

Run the bash shell script ```./test.sh``` to launch python unit test self-discovery after setting the required environment variables.  

#### Manual Curl Tests Scripts

1. create buy order  
    
    ```curl$ ./put_buy_order.sh```

Note:  the combination of (idempotence_key, currency, amount) must be unique  

2. get buy order - first page  
    
    ```curl$ ./get_buy_order.sh```

3. get buy order - get subsequent pages  

    ```curl$ ./get_buy_orders_pass_last_ref.sh```

Note:  `last_reference`  
- refers to the id of the last row on the previous page  
- is explictly returned for each page, for use in retrieving the next page

## Issues 2022-07-05

- need to install pydantic on host machine for tests: pip3 install pydantic
- 