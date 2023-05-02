#!/usr/bin/python3

"""flask"""
from api.v1.views import app_views
from flask import Flask
from flask import make_response
from flask import jsonify
from flask_cors import CORS
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def clean_up(exception=None):
    """terminates session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'error': 'Not found'}), 404
    )


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
