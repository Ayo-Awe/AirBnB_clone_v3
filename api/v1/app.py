#!/usr/bin/python3
"""Flask API server. Serves
a REST API on port 5000 """

import os
from models import storage
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(ctx):
    storage.close()


@app.errorhandler(404)
def resource_not_found(error):
    return {"error": "Not found"}


if __name__ == "__main__":
    port = os.getenv("HBNB_API_PORT") or "0.0.0.0"
    host = os.getenv("HBNB_API_HOST") or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
