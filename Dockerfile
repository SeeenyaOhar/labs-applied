FROM python:3.7
ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'\
  POETRY_VERSION=1.7.1\
  PATH=${PATH}:${POETRY_HOME}

COPY . /code
WORKDIR /code
# RUN apt-get update && apt-get install build-essential
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry install

CMD flask -a api.app run