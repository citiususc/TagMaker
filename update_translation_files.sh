#!/usr/bin/env bash

# From the root folder (TagMaker project)
# Generate translation files
python3.6 manage.py makemessages --locale=es --locale=en --ignore ".venv/*"
python3.6 manage.py makemessages --locale=es --locale=en -d djangojs -e html,js --ignore ".venv/*"