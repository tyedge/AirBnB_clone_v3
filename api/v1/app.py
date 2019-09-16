#!/usr/bin/python3
""" file to connect to API """


from models import storage
from os import getenv
from flask import Flask, Blueprint, make_response, jsonify
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_appcontext(code):
    """ closes storage """
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """ handler for 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')))
