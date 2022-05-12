release: python manage.py migrate
web: gunicorn django_content_downloader.wsgi; python manage.py collectstatic --noinput