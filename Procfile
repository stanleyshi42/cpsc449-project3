user_api: gunicorn --bind=:$PORT --access-logfile - --capture-output user_api:__hug_wsgi__
timeline_api: gunicorn --bind=:$PORT --access-logfile - --capture-output timeline_api:__hug_wsgi__
like_api: gunicorn --bind=:$PORT --access-logfile - --capture-output like_api:__hug_wsgi__
poll_api: gunicorn --bind=:$PORT --access-logfile - --capture-output poll_api:__hug_wsgi__
service_registry: gunicorn --bind=:$PORT --access-logfile - --capture-output service_registry:__hug_wsgi__
