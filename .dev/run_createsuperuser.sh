#!/bin/bash

SERVICE_NAME="django"

# Get the latest built container ID
CONTAINER_ID=$(docker ps --format "{{.ID}} {{.Names}}" --filter "name=$SERVICE_NAME" | awk 'NR==1 {print $1}')

if [[ -z $CONTAINER_ID ]]; then
    echo "No containers found for service: $SERVICE_NAME"
else
    docker exec -it $CONTAINER_ID sh -c "python manage.py createsuperuser"
fi
