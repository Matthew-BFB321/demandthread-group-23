import logging
import os

from flask import Flask, jsonify, request

import db
from api import api
from config import CONFIGS

app = Flask(__name__)
app.config.from_object(CONFIGS[os.getenv("APP_ENV", "development")])
db.init_app(app)
app.register_blueprint(api)

#Warnings and errors are written to app.log with their time
logging.basicConfig(filename="app.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

#One handler for 400, 404 and 500 errors, and it answers with JSON.
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def handle_error(error):
    app.logger.warning("%s on %s", error.code, request.path)
    return jsonify(error=error.name, message=error.description), error.code


# ---------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])