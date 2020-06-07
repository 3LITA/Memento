#!/bin/bash

cd ../

printf "ISORT:\n"
isort app -rc

printf "\nBLACK:\n"
black app --skip-string-normalization

printf "\nFLAKE8:\n"
flake8 app

printf "\nMYPY\n"
mypy app
