#!/usr/bin/env bash

python manage.py makemigrations 
python manage.py migrate 

python manage.py shell <<EOF

from django.contrib.auth import get_user_model
from decouple import config

email = config("SUPERUSER_EMAIL")
password = config("SUPERUSER_PASSWORD")

User = get_user_model()
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF

python manage.py collectstatic --noinput 
gunicorn core.wsgi:application --bind 0.0.0.0:8000