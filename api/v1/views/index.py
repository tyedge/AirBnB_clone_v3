#!/usr/bin/python3
"""index to connect to API"""
from api.v1.views import app_views
from models import storage
from flask import Flask, Blueprint, jsonify

@app_views.route('/status', strict_slashes=False)
def jsonify_status():
    ''' sets status '''
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass
