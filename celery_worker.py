
from celery import Celery
from app import create_app

# Create Flask app
flask_app = create_app()

# Create Celery app
celery = Celery(
    flask_app.import_name,
    broker='redis://localhost:6379/0',
)

# Load config from Flask app into Celery
celery.conf.update(flask_app.config)

# Attach Flask context to Celery tasks
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
