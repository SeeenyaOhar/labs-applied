FROM python:3.8.10 AS builder
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx python3-venv
ENV PATH="/root/.local/bin:${PATH}"
RUN pipx install poetry
RUN pipx inject poetry poetry-plugin-bundle
WORKDIR /code
COPY pyproject.toml poetry.lock README.md ./
RUN poetry env use 3.8.10
RUN poetry bundle venv --only=main --python=/usr/local/bin/python3 /venv

FROM python:3.8.10-slim AS app
ENV PATH="$PATH:/code/venv/bin"
RUN apt-get update && apt-get install libpq5 -y
COPY . /code
COPY --from=builder /venv /code/venv
WORKDIR /code
CMD ["/bin/bash", "./docker-entrypoint.sh"]