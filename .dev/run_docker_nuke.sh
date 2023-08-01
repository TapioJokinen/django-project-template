#!/bin/bash

# Stop all running Docker containers
docker stop $(docker ps -aq)

docker system prune -af

docker volume prune -af
