import os 
from api import create_app

'''
runner file to create application api 
'''

config_name = os.environ.get('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__': 
  app.run()
