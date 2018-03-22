from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

import config
from .views import api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.register_blueprint(api, url_prefix='/')
