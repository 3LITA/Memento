#!/bin/bash

cd ../../
pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel update -i messages.pot -d app/i18n
rm messages.pot
