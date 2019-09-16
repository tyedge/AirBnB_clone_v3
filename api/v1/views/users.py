#!/usr/bin/python3
""" This module contains the views for Amenities """


from api.v1.views import app_views
from flask import (
    jsonify, request, abort, make_response
)
import models


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """ This function gets a list of all users """
    all_users = []
    for u in models.storage.all("User").values():
        all_users.append(u.to_dict())
    ret = jsonify(all_users)
    return ret


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def single_user(user_id):
    """ This function retrieves info for a selected user """
    single_user = models.storage.get("User", user_id)
    if single_user is None:
        abort(404)
    ret = jsonify(single_user.to_dict())
    return ret


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def user_remover(user_id):
    """ This function deletes a user object """
    rm_user = models.storage.get("User", user_id)
    if rm_user is None:
        abort(404)
    rm_user.delete()
    models.storage.save()
    ret = jsonify({})
    return ret


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def user_creator():
    """ This function creates a new user object """
    response = request.get_json()
    if response is None:
        retval = jsonify(error="Not a JSON")
        return make_response(retval, 400)
    if "email" not in response:
        retval = jsonify(error="Missing email")
        return make_response(retval, 400)
    if "password" not in response:
        retval = jsonify(error="Missing password")
        return make_response(retval, 400)
    cr_user = models.user.User(**response)
    cr_user.save()
    retval = jsonify(cr_user.to_dict())
    return make_response(retval, 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def user_updater(user_id):
    """ This function updates a user object """
    response = request.get_json()
    if response is None:
        retval = jsonify(error="Not a JSON")
        return make_response(retval, 400)
    updater = models.storage.get("User", user_id)
    if updater is None:
        abort(404)
    for k, v in response.items():
        if k not in ("id", "created_at", "updated_at", "email"):
            setattr(updater, k, v)
    updater.save()
    retval = jsonify(updater.to_dict())
    return retval
