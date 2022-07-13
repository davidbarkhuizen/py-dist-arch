# 12-factor Python Micro Service Architecture

## Important Note on Authentication, Security & Data Persistence

This demonstration system features no authentication, has not been secured, and is not intended for production use.  Furthermore, no guarantees are made as no data persistence.  While reasonable efforts have been mad eto source components from reputable sources, you use this system entirely at your own risk, and the author accepts no responsibility whatsoever for its use or misuse.

## Functional Requirements

API allows its clients to manage BTC buy orders. Clients place orders to purchase BTC for fiat at a market price. API does not create transactions on the Bitcoin blockchain, but simply stores the order information in its database for further processing.

### Create Buy Order

1. Creation of a Buy Order requires the following data at minimum:

* currency - represents the currency (ISO3 code one of: EUR, GBP, USD)
* amount - represents the amount of currency (0 < x < 1,000,000,000)

2. Successful call should store the order in the database. The following info should be
stored at a minimum:

* id - order's unique identifier
* amount - requested fiat amount
* currency - requested fiat currency
* exchange rate - value of BTC versus the requested fiat; BTC is the base currency and requested fiat is the quote currency; use the third-party API to source the exchange rates
* bitcoin amount - amount of BTC which the requested amount of fiat buys at the exchange rate. Use a precision of 8 decimal digits, and always round up. Do not lose precision in calculations

3. Buy Order creation must be idempotent.

4. Sum of bitcoin amount of all orders stored in the system must not exceed 100BTC.

System must not allow creation of new orders which would cause the constraint to be violated.

### Fetch Buy Order Collection

Returns Buy Orders stored in the database in reverse chronological order.

Resources must have the following attributes at minimum: id, amount, currency, exchange rate, bitcoin amount. Responses must be paged. Response time should be the same regardless which page is requested.

## Architecture

### Component Technologies

|aspect|technology|
|------|----------|
|Database|Postgres|
|ORM|SqlAlchemy|
|Models|Pydantic|
|REST server|FastAPI|
|Queue|RabbitMQ (pika)|
|Structured Event Logging|FluentD|

### 12 Factor App Methodology

This system attempts to fulfill the [12 factor app methodology](https://12factor.net/):

|Factor|Requirement|
|------|-----------|
Codebase|There should be exactly one codebase for a deployed service with the codebase being used for many deployments
Dependencies|All dependencies should be declared, with no implicit reliance on system tools or libraries
Config|Configuration that varies between deployments should be stored in the environment
Backing services|All backing services are treated as attached resources and attached and detached by the execution environment
Build, release, run|The delivery pipeline should strictly consist of build, release, run
Processes|Applications should be deployed as one or more stateless processes with persisted data stored on a backing service
Port binding|Self-contained services should make themselves available to other services by specified ports
Concurrency|Concurrency is advocated by scaling individual processes
Disposability|Fast startup and shutdown are advocated for a more robust and resilient system
Dev/Prod parity|All environments should be as similar as possible
Logs|Applications should produce logs as event streams and leave the execution environment to aggregate
Admin Processes|Any needed admin tasks should be kept in source control and packaged with the application

### Write/Read Model

The architecture splits the data persistence into a write model and a read model.  The write model is intended as the golden source of truth.  The read model is kept in sync with the write model using an event service (queue).  This allows the write model table structures to be optimized for fast insert and update, whereas by contrast the read model table structures are optimized for fast read.

### Containerisation

- docker-compose used for container management ```./docker-compose.yml```  
- default environment settings file ```.env```
- where possible Alpine linux based images have been used to reduce image size and attack surface

#### External Docker Base Images

image|technology|docker service
-----|----------|--------
postgres:13.4-alpine|postgres database|read_model, write_model
fluent/fluentd:v1.13.0-1.0|fluentd event logger|log
rabbitmq:3.9-management-alpine|rabbitmq queue|queue
tiangolo/uvicorn-gunicorn:python3.8-alpine3.10|python fastapi|btc_price, create_buy_order, fetch_buy_orders, migration, read_model_sync

#### Container Build

The container build process is broken into 2 stages: base images and run images.  

build stage|shell script
-----------|------------------------
base images|```./build_base_images.sh```
run images|```./build_run_images.sh```  

##### Base Image

The base image for a service has all requirements and depencies for that service installed, but no code.  

Using the migration service as an example, the following pattern is adhered to:

1. use minimal alphine image as external base  
2. install os package level dependencies using os package manager (apt, snap)  
3. install and upgrade pip  
4. install python packages  

```docker/services/migration/Dockerfile.base```
```
FROM python:3.8.2-alpine
WORKDIR /xapo
RUN apk update
RUN apk add linux-headers musl-dev build-base gcc python-dev postgresql-dev curl
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY codebase/services/migration/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
```

##### Run Image

The run image is simply the base image with the codebase installed and ready to execute.  

```docker/services/migration/Dockerfile```
```
FROM migration_base:001
WORKDIR /xapo
COPY codebase/ ./codebase/
WORKDIR /xapo/codebase/
CMD ["python", "migration_service.py"]
```

This split allows the run image to rebuilt at minimum cost, but does mean that when python module dependencies change the base image must be rebuilt.  

#### Create Request Idempotence

A specific requirement was around idempotence of create requests, and there is some complication in the database structure which supports this.  

### Docker Services

name|service|technologies
----|-------|------------
log|structured event logging|fluentd
write_model|write data model|postgresql
read_model|read data model|postgresql
migration|database migration|postgresql, yoyo migrations, fastapi
queue|event/message queues|rabbitmq
read_model_sync|update read data model from queue|rabbitmq,postgresql
btc_price|fetch btc price from external api|external coinbase api
create_buy_order|accept and fulfill create new buy order http requests|
fetch_buy_orders|accept and fulfill create new buy order http requests|

create_buy_order exposed @ PUT http://localhost:8777/buy_order
fetch_buy_orders exposed @ GET http://localhost:8778/buy_orders

## Setup & Installation

### Host Machine Pre-Requisites

1. Docker, Docker-Compose
2. curl
3. python3  
4. pydantic pip3 module `sudo pip3 install pydantic`

### Build & Launch Cluster

Assuming that docker-compose is running on the host machine, execute the following shell scripts from the repo root:  

        ./build_base_images.sh
        ./build_run_images.sh
        ./run.sh

Run the tests to confirm that everything is up and running ok, launch python unit test discovery:  

        ./test.sh```

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
