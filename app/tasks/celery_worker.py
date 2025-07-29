from celery import Celery
from app import create_app

# Step 1: Create Flask app
flask_app = create_app()

# Step 2: Create Celery app
celery = Celery(
    flask_app.import_name,
    broker='redis://localhost:6379/0',
)

# Step 3: Load Flask app config into Celery
celery.conf.update(flask_app.config)

# Step 4: Attach Flask context to Celery tasks
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

from app.tasks import sync_cars  # this is mandatory!