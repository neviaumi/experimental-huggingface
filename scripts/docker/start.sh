#!/usr/bin/env bash

set -ex
LLM_PORT="${PORT:-$LLM_PORT}"

pdm run python ./src/experimental_huggingface/main.py