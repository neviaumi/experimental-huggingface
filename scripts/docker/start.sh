#!/usr/bin/env bash

set -ex
LLM_PORT="${PORT:-$LLM_PORT}"

pdm run uvicorn --app-dir src/experimental_llm_agent --host 0.0.0.0 --port $LLM_PORT llama:app