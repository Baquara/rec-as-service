from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
from sqlalchemy_utils import database_exists, create_database
sys.path.append(".")



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()
db.session.commit()
ma = Marshmallow(app)
migrate = Migrate(app, db)


from .models import users
from .routes import routes