# Builder Stage
FROM ghcr.io/abetlen/llama-cpp-python:v0.3.1

WORKDIR /app

ENV PDM_CHECK_UPDATE=false
COPY .models/phi-3.5 ./.models/phi-3.5
COPY pyproject.toml pdm.lock .python-version ./
COPY ./src/ ./src/
COPY ./tests/ ./tests/
COPY ./scripts/docker/ ./scripts/docker/

RUN bash ./scripts/docker/setup.sh