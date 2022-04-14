# Development Notes

## docker, docker-swarm installation on linux (ubuntu 21.??)

sudo apt-get install docker-ce=5:20.10.8~3-0~ubuntu-hirsute docker-ce-cli=5:20.10.8~3-0~ubuntu-hirsute containerd.io

docker build -t restserver:001 .
docker run -dp 3000:3000 restserver:001

docker logs $containerid -f

docker inspect --format "{{json .State.Health }}" 2aff56a67da2 | jq

docker cp <containerId>:/file/path/within/container /host/path/target

uvicorn test:app --reload

## Tech Stack

### language

python 3.?

### (python) web server - fastapi

[fastapi](https://github.com/tiangolo/fastapi) chosen over flask, due to promise of increased performance
=> docker image https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

postgresql docker image

https://hub.docker.com/_/postgres

ubuntu

sudo apt-get install libpq-dev

### logging - fluentd 

/fluentd/etc/fluent.conf

define <match fluent.**> to capture fluentd logs in top level is deprecated. Use <label @FLUENT_LOG> instead

### database - postgresql

db     | Error: Database is uninitialized and superuser password is not specified.
db     |        You must specify POSTGRES_PASSWORD to a non-empty value for the
db     |        superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".


db    | The database cluster will be initialized with locale "en_US.utf8".
db    | The default database encoding has accordingly been set to "UTF8".
db    | The default text search configuration will be set to "english".

$ sudo su - postgres
$ psql -f /home/david/code/xapo/codebase/model/migrations/write_model/001_base.sql 

# rabbitmq

not secured

management web console
http://localhost:15672/
guest, guest

## yoyo

yoyo apply --database postgresql://scott:tiger@localhost/db ./migrations