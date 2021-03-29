import json 
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

  @app.route('/users', methods=['Post'])
  def create_user():
    payload = json.loads(request.data)

    user = User(
            email=payload['email'],
            first_name=payload['first_name'],
            last_name=payload['last_name']
          )
    user.insert()

    return {
      'success': True,
      'id': user.id,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email
    }, 201
    
  return app 
