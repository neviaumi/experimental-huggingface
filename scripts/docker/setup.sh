#!/usr/bin/env bash

set -ex
apt-get update -y
apt-get install -y python3-pip
pip3 install -U pdm
pdm install
