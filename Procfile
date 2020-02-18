web: flask db upgrade; flask translate compile; gunicorn pi:app
worker: rq worker -u $REDIS_URL product-importer-tasks