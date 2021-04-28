GUNICORN_FLAGS=--reload
GUNICORN_WORKERS=1
GUNICORN_PORT=5001

gunicorn $GUNICORN_FLAGS --access-logfile - --worker-class sync --chdir .. --workers=$GUNICORN_WORKERS -b :$GUNICORN_PORT main_flask:flask_app
