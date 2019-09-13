#!/usr/bin/python3
"""index to connect to API"""
from api.v1.views import app_views
from models import storage
from flask import Flask, Blueprint, jsonify

FileToChange = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}

@app_views.route('/status', strict_slashes=False)
def jsonify_status():
    ''' sets status '''
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def Stats():
    """stats"""
    return_dict = {}
    for key, value in FileToChange.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)

if __name__ == "__main__":
    pass
