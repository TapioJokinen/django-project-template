# Django backend template

## Getting started

---

*This project uses [Poetry](https://python-poetry.org/) for python packaging and dependency management.*

1. Create virtual environment:

    ```bash
    poetry shell
    ```

2. Install packages:

    ```bash
    poetry install
    ```

3. Run project in Docker:

    ```bash
    ./.dev/run_dev.sh -B
    ```

4. Run migrations:
    ```bash
    ./.dev/run_migrations.sh
    ```

## Having trouble?

### Postgres healthcheck fails?
>Make sure the EOL for files .env and postgres_healthcheck.sh is LF and not CRLF.