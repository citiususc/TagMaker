#!/usr/bin/env bash

# From the root folder (TagMaker project)
# Generate translation files
python3 manage.py makemessages --locale=es --locale=en --ignore ".venv/*"
python3 manage.py makemessages --locale=es --locale=en -d djangojs -e html,js --ignore ".venv/*"

# Update translation files in TagMaker/locale.
# ...

# Compile translation files
cd TagMaker && python3 ../manage.py compilemessages && cd ..