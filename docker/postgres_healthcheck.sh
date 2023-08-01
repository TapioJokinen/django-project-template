#!/bin/bash

set -e

# Read each line in the .env file
while IFS= read -r line || [[ -n "$line" ]]; do
  # Skip empty lines and lines starting with #
  if [[ -n "$line" && ! "$line" =~ ^\s*# ]]; then
    # Export the variable
    export "$line"
  fi
done < ".env"

until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" --username="$POSTGRES_USER" dbname="$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done


# Read each line in the .env file
while IFS= read -r line || [[ -n "$line" ]]; do
  # Skip empty lines and lines starting with #
  if [[ -n "$line" && ! "$line" =~ ^\s*# ]]; then
    # Export the variable
    export "$line"
  fi
done < ".env"

exec "$@"
