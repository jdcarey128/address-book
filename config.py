import os 

class Config: 
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'super secret key'
  SQLALCHEMY_TRACK_MODIFICATIONS = False 
  SQLALCHEMY_RECORD_QUERIES = True 

class DevelopmentConfig(Config): 
  DEBUG = True 
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/address_book_development'

class TestingConfig(Config):
  DEBUG = True 
  TESTING = True 
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/address_book_test'

class ProductionConfig(Config):
  DEBUG = False 
  TESTING = False
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig,

  'default': DevelopmentConfig
}
