#!/usr/bin/env bash
flask db init
flask db migrate
flask db upgrade
#python -m flask run
python3 app.py
