
from flask import Flask

from api import mapper_configs_bp
app = Flask(__name__)
app.register_blueprint(mapper_configs_bp)


if __name__ == "__main__":
  app.run(host="0.0.0.0")

