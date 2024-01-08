#!/usr/bin/python3
"""states api handling"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route("/api/v1/states<state_id>/cities", methods=["GET"])
def city_state_list(state_id):
    """retrieves the list of all city state objects"""
    state = State.query.get(state_id)
    if state:
        cities = state.cities()
        new_list = [city.to_dict() for city in cities]
        return jsonify(new_list)
    else:
        abort(404)


@app_views.route("/api/v1/cities/<city_id>", methods=["GET"])
def city_with_id(city_id):
    """retrieves states based on id"""
    city = City.query.get(city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)

@app_views.route("/api/v1/cities/<city_id>")
def delete_city(city_id):
    """deletes city based on its id"""
    city = City.query.get(city_id)

    if city:
        storage.delete(city)
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route("/api/v1/cities", methods=["POST"])
def create_new_state():
    """creates a new state from user"""
    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in list(data.keys()):
        abort(400, "Missing name")

    new_city = State(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route("PUT /api/v1/cities/<city_id>", methods=["PUT"])
def update_state(city_id):
    """updates states bases on state id"""
    city = City.query.get(city_id)
    if city:
        if not request.get.json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
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