#!/bin/bash
extra_options=""
if [[ $DEBUG != "false" ]]; then
    extra_options="--reload"
fi

poetry run alembic upgrade head &&\
poetry run uvicorn app.main:app --host 0.0.0.0 ${extra_options}
