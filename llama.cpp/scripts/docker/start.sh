#!/usr/bin/env bash

set -ex
export LLAMA_ARG_PORT="${PORT:-$LLAMA_CPP_PORT}"
export LLAMA_ARG_MODEL="model/Phi-3.5-mini-instruct-Q4_K_M.gguf"
/llama-server --log-disable