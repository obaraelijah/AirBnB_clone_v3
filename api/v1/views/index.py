#!/usr/bin/python3
""" Index """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """ returns Status of API """
    return jsonify({"status": "OK"})

@app_views.route('stats', strict_slashes=False)
def stats():
    """ returns number of each object by type """
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models.amenity import Amenity
    from models import storage

    classes = {"amenities": Amenity, "cities": City,"places": Place,
                "reviews": Review, "states": State, "users": User}
    count_dict = {}
    for key, value in classes.items():
        count_dict[key] = storage.count(value)
    return jsonify(count_dict)