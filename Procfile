release: python manage.py migrate && python manage.py create_admin && python manage.py collectstatic --noinput
web: gunicorn senescence.wsgi:application --bind 0.0.0.0:$PORT
