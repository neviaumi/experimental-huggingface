# Builder Stage
FROM python:3.12.4-slim AS base

WORKDIR /app

ENV PDM_CHECK_UPDATE=false
COPY pyproject.toml pdm.lock .python-version ./
COPY ./src/ ./src/
COPY ./tests/ ./tests/
COPY ./scripts/docker/ ./scripts/docker/

RUN bash ./scripts/docker/setup.sh