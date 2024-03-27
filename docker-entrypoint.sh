#!/bin/bash
source ./venv/bin/activate
BACK_VAR=$(pwd)
cd alembic && ../venv/bin/python -m alembic upgrade head
cd .. && ./venv/bin/python -m flask --app api.app run --host=0.0.0.0