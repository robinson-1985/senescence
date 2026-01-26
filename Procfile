release: mkdir -p staticfiles && python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn senescence.wsgi:application --bind 0.0.0.0:$PORT
