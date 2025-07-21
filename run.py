import os
import sys

# Make sure Python can find the app/ directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 