#!/bin/bash

docker compose -f docker-compose.dev.yml down

if [ $# -eq 0 ]; then
    docker compose -f docker-compose.dev.yml up
fi

if [ "$1" = "-b" ] || [ "$1" = "-B" ]; then
    docker compose -f docker-compose.dev.yml build --no-cache
    docker compose -f docker-compose.dev.yml up
fi
