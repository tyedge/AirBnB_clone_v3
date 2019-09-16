#!/usr/bin/python3

""" This modules contains the views for Cities """


from api.v1.views import app_views
from flask import (
    jsonify, request, abort, make_response
)
import models


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def all_cities(state_id):
    """ This function gets a list of all cities in a specified state """
    single_state = models.storage.get("State", state_id)
    if single_state is None:
        abort(404)
    cities = []
    for city in models.storage.all("City").values():
        if city.state_id == state_id:
            cities.append(city.to_dict())
    ret = jsonify(cities)
    return ret


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def single_city(city_id):
    """ This function retrieves info for a single city """
    single_city = models.storage.get("City", city_id)
    if single_city is None:
        abort(404)
    ret = jsonify(single_city.to_dict())
    return ret


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def city_remover(city_id):
    """ This function deletes a city object """
    rm_city = models.storage.get("City", city_id)
    if rm_city is None:
        abort(404)
    rm_city.delete()
    models.storage.save()
    ret = jsonify({})
    return ret


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def city_creator(state_id):
    """ This function creates a new city object """
    single_state = models.storage.get("State", state_id)
    if single_state is None:
        abort(404)
    response = request.get_json()
    if response is None:
        retval = jsonify(error="Not a JSON")
        return make_response(retval, 400)
    if "name" not in response:
        retval = jsonify(error="Missing name")
        return make_response(retval, 400)
    cr_city = models.city.City(**response)
    cr_city.state_id = state_id
    cr_city.save()
    retval = jsonify(cr_city.to_dict())
    return make_response(retval, 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def city_updater(city_id):
    """ This function updates a city object """
    response = request.get_json()
    if response is None:
        retval = jsonify(error="Not a JSON")
        return make_response(retval, 400)
    updater = models.storage.get("City", city_id)
    if updater is None:
        abort(404)
    for k, v in response.items():
        if k not in ("id", "created_at", "updated_at"):
            setattr(updater, k, v)
    updater.save()
    retval = jsonify(updater.to_dict())
    return retval
