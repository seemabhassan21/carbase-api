from flask import Flask
from app.config import Config
from app.extensions import db, jwt, ma, migrate
from app.routes import all_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    for bp, prefix in all_blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app
