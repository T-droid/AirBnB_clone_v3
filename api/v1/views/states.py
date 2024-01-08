#!/usr/bin/python3
"""states api handling"""
from flask import jasonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/api/v1/states", methods=["GET"])
def state_list():
    """retrieves the list of all state objects"""
    states = storage.all(State).values()
    new_list = [state.do_dict() for state in states]
    return jasonify(new_list)

@app_views.route("/api/v1/states/<state_id>", methods=["GET"])
def state_with_id(state_id):
    """retrieves states based on id"""
    state = State.query.get(state_id)
    if state:
        return jasonify(state.to_dict())
    else:
        abort(404)

@app_views.route("/api/v1/states/<state_id>")
def delete_state(state_id):
    """deletes state based on its id"""
    state = State.query.get(state_id)

    if state:
        storage.delete(state)
        return jasonify({}), 200
    else:
        abort(404)

@app_views.route("/api/v1/states", methods=["POST"])
def create_new_state():
    """creates a new state from user"""
    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in list(data.keys()):
        abort(400, "Missing name")

    new_state = State(**data)
    state.save()
    return jasonify(state.to_dict()), 201

@app_views.route("PUT /api/v1/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """updates states bases on state id"""
    state = State.query.get(state_id)
    if state:
        if not request.get.json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


# Error Handlers
@app_views.errorhandler(404)
def not_found(error):
    """ Handles the 404 code """
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def bad_request(error):
    """ Handles the 400 status code """
    response = {'error': 'Bad Request'}
    return jsonify(response), 400