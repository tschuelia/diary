export PYTHONPATH=/app/diary:/hetzner
export DJANGO_SETTINGS_MODULE=settings_prod

cd /app/diary

/app/venv/bin/django-admin migrate

/app/venv/bin/gunicorn \
  --log-level info \
  --bind 0.0.0.0:5000 \
  diaryWebsite.wsgi:application
