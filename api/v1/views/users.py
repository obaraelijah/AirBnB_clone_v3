#!/usr/bin/python3
""" Users view """

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ retrieve all users """
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route(
    '/users/<user_id>',
    methods=['GET'],
    strict_slashes=False
    )
def get_user(user_id):
    """ retrieve a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_user(user_id):
    """ deletes a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a user object"""
    if not request.get_json:
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    user = User(**request.get_json())
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def put_user(user_id):
    """ update user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json:
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())
