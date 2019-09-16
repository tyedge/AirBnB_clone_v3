#!/usr/bin/python3
""" This module contains the views for Amenities """


from api.v1.views import app_views
from flask import (
    jsonify, request, abort, make_response
)
import models


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amens():
    """ This function gets a list of all amenities """
    all_amens = []
    for amen in models.storage.all("Amenity").values():
        all_amens.append(amen.to_dict())
    ret = jsonify(all_amens)
    return ret


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def single_amen(amenity_id):
    """ This function retrieves info for a selected amenity """
    single_amen = models.storage.get("Amenity", amenity_id)
    if single_amen is None:
        abort(404)
    ret = jsonify(single_amen.to_dict())
    return ret


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def amenity_remover(amenity_id):
    """ This function deletes an amenity object """
    rm_amen = models.storage.get("Amenity", amenity_id)
    if rm_amen is None:
        abort(404)
    rm_amen.delete()
    models.storage.save()
    ret = jsonify({})
    return ret


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def amenity_creator():
    """ This function creates a new amenity object """
    response = request.get_json()
    if response is None:
        retval = jsonify(error="Not a JSON")
        return make_response(retval, 400)
    if "name" not in response:
        retval = jsonify(error="Missing name")
        return make_response(retval, 400)
    cr_amen = models.amenity.Amenity(**response)
    cr_amen.save()
    retval = jsonify(cr_amen.to_dict())
    return make_response(retval, 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def amenity_updater(amenity_id):
    """ This function updates an amenity object """
    response = request.get_json()
    if response is None:
        retval = jsonify(error="Not a JSON")
        return make_response(retval, 400)
    updater = models.storage.get("Amenity", amenity_id)
    if updater is None:
        abort(404)
    for k, v in response.items():
        if k not in ("id", "created_at", "updated_at"):
            setattr(updater, k, v)
    updater.save()
    retval = jsonify(updater.to_dict())
    return retval
