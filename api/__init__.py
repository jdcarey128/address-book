import json 
from flask_cors import CORS
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

  CORS(app, resources={r"/*": {"origins": "*"}})

  api = Api(app)

  @app.after_request 
  def after_request(response):
    '''
    CORS setup 
    '''
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')

    return response 
  
  from api.resources.users import UsersResource, UserResource
  from api.resources.contacts import ContactsResource, ContactResource
  from api.resources.login import LoginResource

  api.add_resource(UserResource, '/users/<user_id>')
  api.add_resource(UsersResource, '/users')
  api.add_resource(ContactsResource, '/users/<user_id>/contacts')
  api.add_resource(ContactResource, '/users/<user_id>/contacts/<contact_id>')
  api.add_resource(LoginResource, '/login')

  return app 
