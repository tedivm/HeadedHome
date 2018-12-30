#!/usr/bin/env bash

source env/bin/activate
source config.sh

python -m app "$@"
