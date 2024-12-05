clear

export $(cat .env | xargs) &&  docker-compose -f docker-compose.yml --env-file .env up 