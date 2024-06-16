from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import config


db = SQLAlchemy()


def create_app(config_name):
    """
    For to use dynamic environment.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.firewalls.routes import firewalls
    from app.main.routes import main
    from app.policies.routes import policies
    from app.rules.routes import rules

    app.register_blueprint(firewalls)
    app.register_blueprint(main)
    app.register_blueprint(policies)
    app.register_blueprint(rules)

    return app
