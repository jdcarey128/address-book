from flask import Flask 
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy

# local imports 
from config import config 

db = SQLAlchemy()

def create_app(config_name = 'default'): 
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  from api.database import models

  db.init_app(app)
  migrate = Migrate(app, db)
  
  @app.route('/')
  def index(): 
    return 'Hello Joshua'

  return app 
