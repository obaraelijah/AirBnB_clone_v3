#!/usr/bin/python3

""" Handles all restful API actions for States in rest api project"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities_by_state(state_id):
    """retrieve cities based on state_id"""
    state_obj = storage.all(State)
    states = [obj for obj in state_obj.values()]

    if request.method == 'GET':
        for state in states:
            if state.id == state_id:
                cities_objs = storage.all(City)
                cities = [obj.to_dict() for obj in
                          cities_objs.values() if obj.state_id == state_id]
                return jsonify(cities)
        abort(404)
    elif request.method == 'POST':
        for state in states:
            if state.id == state_id:
                my_dict = request.get_json()
                if my_dict is None:
                    abort(400, 'Not a JSON')
                if my_dict.get("name") is None:
                    abort(400, 'Missing name')
                my_dict["state_id"] = state_id
                city = City(**my_dict)
                city.save()
                return jsonify(city.to_dict()), 201

@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def city_by_city_id(city_id):
    """retrieves cities by cities id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        city.name = my_dict.get("name")
        city.save()
        return jsonify(city.to_dict()), 200
