#!/bin/sh
set -e

git status >/dev/null
pwd | grep -c space-invaders >/dev/null

black -l 78 .
isort .
flake8 --ignore=E203,W503
# https://github.com/PyCQA/pycodestyle/issues/373
# https://www.flake8rules.com/rules/W503.html
