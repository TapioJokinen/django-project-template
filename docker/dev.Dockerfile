# builder
FROM python:3.11.4-slim-bookworm as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry psycopg2

WORKDIR /usr/myapp

COPY poetry.lock pyproject.toml /usr/myapp/

RUN poetry config virtualenvs.create false \
    && poetry install $(test "$DJANGO_SETTINGS_MODULE" == config.django.production && echo "--no-dev") --no-interaction --no-ansi --no-root


# runner
FROM python:3.11.4-slim-bookworm as runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y \
    postgresql \
    libmagic1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/myapp

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . /usr/myapp

ENTRYPOINT [ "./docker/postgres_healthcheck.sh" ]
