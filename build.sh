#!/usr/bin/env bash

pip install -r requirements.txt

python download_model.py

python manage.py collectstatic --noinput

python manage.py migrate