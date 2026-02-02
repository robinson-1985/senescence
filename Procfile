release: python manage.py migrate && python scripts/ensure_admin.py && python manage.py collectstatic --noinput
web: gunicorn senescence.wsgi:application --bind 0.0.0.0:$PORT
