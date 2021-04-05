import json 
from flask import request 
from flask_restful import Resource, abort 

from api import db 
from api.database.models import User 
from . import _validate_field, _error_response
from sqlalchemy.orm.exc import NoResultFound

def _user_payload(user):
  return {
    'id': user.id,
    'first_name': user.first_name,
    'last_name': user.last_name,
    'email': user.email
  }

class LoginResource(Resource):
  def post(self):
    proceed = True 
    errors = []

    data = json.loads(request.data)
    proceed, user_email, errors = _validate_field(
      data, 'email', proceed, errors)

    if proceed: 
      try: 
        user = db.session.query(User).filter_by(email=user_email).one()
      except NoResultFound:
        return abort(404)
    else: 
      return _error_response(errors, 400)
    
    user_payload = _user_payload(user)
    user_payload['success'] = True
    return user_payload, 200
