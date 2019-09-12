#!/usr/bin/python3
"""file to connect to API"""
from models import storage
from os import getenv
from flask import Flask, Blueprint
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(code):
    "closes storage"
    storage.close()

@app.errorhandler(404)
def errorhandler(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')))
