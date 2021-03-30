import json 
from flask_restful import Api
from flask import Flask, request
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy

# local imports 
from config import config 

db = SQLAlchemy()

def create_app(config_name = 'default'): 
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  from api.database.models import User, Contact

  db.init_app(app)
  migrate = Migrate(app, db)
  
  @app.route('/')
  def index(): 
    return 'Hello Joshua'

  api = Api(app)
  
  from api.resources.users import UsersResource, UserResource

  api.add_resource(UserResource, '/users/<user_id>')
  api.add_resource(UsersResource, '/users')

  return app 
