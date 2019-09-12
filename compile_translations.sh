#!/usr/bin/env bash

# Compile translation files
cd TagMaker && ../venv/bin/python3.6 ../manage.py compilemessages && cd ..