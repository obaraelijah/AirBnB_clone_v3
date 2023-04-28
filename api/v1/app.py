#!/usr/bin/python3

"""flask"""
from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def clean_up(exception=None):
    """terminates session"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, threaded=True)
