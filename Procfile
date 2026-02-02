release: /app/.venv/bin/python manage.py migrate && /app/.venv/bin/python manage.py create_admin && /app/.venv/bin/python manage.py collectstatic --noinput
web: gunicorn senescence.wsgi:application --bind 0.0.0.0:$PORT
