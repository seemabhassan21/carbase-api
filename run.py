import os
import sys

# Ensure the 'app/' directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from celery_worker import celery

# Create Flask app
app = create_app()

# Attach Celery to Flask app context (if needed for tasks)
celery.set_default()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
