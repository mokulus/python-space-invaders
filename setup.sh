#!/bin/sh

python -m virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
