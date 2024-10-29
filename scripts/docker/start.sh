#!/usr/bin/env bash

set -ex
LLM_PORT="${PORT:-$LLM_PORT}"

pdm run uvicorn --app-dir src/experimental_llama_cpp --host 0.0.0.0 --port $LLM_PORT server:app