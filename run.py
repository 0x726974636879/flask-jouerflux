import os

from flasgger import Swagger

from app import create_app, config, db
from app.constants import ENV


app = create_app(config_name=ENV)
swagger = Swagger(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=config[ENV])
