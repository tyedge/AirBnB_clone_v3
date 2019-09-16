#!/usr/bin/python3

""" This modules contains the views for States """


from api.v1.views import app_views
from flask import (
    jsonify, request, abort, make_response
)
import models


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """ This function gets a list of all states """
    stater = []

    for state in models.storage.all("State").values():
        stater.append(state.to_dict())

    ret = jsonify(stater)
    return ret


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def single_state(state_id):
    """ This function retrieves info for a single state """
    single_state = models.storage.get("State", state_id)
    if single_state is None:
        abort(404)
    ret = jsonify(single_state.to_dict())
    return ret


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def state_remover(state_id):
    """ This function deletes a state object """
    rm_state = models.storage.get("State", state_id)
    if rm_state is None:
        abort(404)
    rm_state.delete()
    models.storage.save()
    ret = jsonify({})
    return ret


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_creator():
    """ This function creates a new state object """
    response = request.get_json()
    if response is None:
        retval = jsonify(error="Not a JSON")
        return make_response(retval, 400)
    if "name" not in response:
        retval = jsonify(error="Missing name")
        return make_response(retval, 400)
    cr_state = models.state.State(**response)
    cr_state.save()
    retval = jsonify(cr_state.to_dict())
    return make_response(retval, 201)


@app_views.route('/states/<string:state_id>', strict_slashes=False,
                 methods=['PUT'])
def state_updater(state_id):
    """ This function updates a state object """
    response = request.get_json()
    if response is None:
        retval = jsonify(error="Not a JSON")
        return make_response(retval, 400)
    updater = models.storage.get("State", state_id)
    if updater is None:
        abort(404)
    for k, v in response.items():
        if k not in ("id", "created_at", "updated_at"):
            setattr(updater, k, v)
    updater.save()
    retval = jsonify(updater.to_dict())
    return retval
