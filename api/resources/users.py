import json 
from flask import request
from flask_restful import Resource

from api import db 
from api.database.models import User

class UsersResource(Resource): 

  def post(self):
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
