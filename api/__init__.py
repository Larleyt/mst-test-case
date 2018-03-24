from flask import (
    Flask,
    jsonify,
    make_response,
    redirect
)
from flask_sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from .views import api
app.register_blueprint(api, url_prefix='/api')


# basic views
@app.errorhandler(400)
def bad_request(error):
    return make_response(
        jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'error': 'Not Found'}), 404)


@app.errorhandler(415)
def unsupported_media_type(error):
    return make_response(
        jsonify({'error': 'Unsupported Media Type'}), 415)
