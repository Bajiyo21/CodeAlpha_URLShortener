#!/bin/bash

pip install --disable-pip-version-check -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate