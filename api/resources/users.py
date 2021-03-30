import json 
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api import db 
from api.database.models import User

def _validate_field(data, field, proceed, errors, missing_okay=False):
  if field in data: 
    data[field] = data[field].strip()
    if len(data[field]) == 0:
      proceed = False 
      errors.append(f"required '{field}' parameter is blank")
  if not missing_okay and field not in data:
    proceed = False 
    errors.append(f"required '{field}' parameter is missing")
    data[field] = ''
  if missing_okay and field not in data: 
    return proceed, None, errors

  return proceed, data[field], errors

def _user_payload(user):
  return {
    'id': user.id,
    'first_name': user.first_name,
    'last_name': user.last_name,
    'email': user.email
  }


class UsersResource(Resource): 
  def _create_user(self, data):
    proceed = True 
    errors = []

    proceed, first_name, errors = _validate_field(
      data, 'first_name', proceed, errors)
    proceed, last_name, errors = _validate_field(
      data, 'last_name', proceed, errors)
    proceed, email, errors = _validate_field(
      data, 'email', proceed, errors)

    if proceed:
      try: 
        user = User(
              email=email,
              first_name=first_name,
              last_name=last_name
            )
        user.insert()
      except IntegrityError: 
        user = None 
        errors.append("email is already taken")

      return user, errors 
    else: 
      return None, errors 

  def post(self):
    user, errors = self._create_user(json.loads(request.data))
    if user is not None: 
      user_payload = _user_payload(user)
      user_payload['success'] = True 
      return user_payload, 201
    else: 
      return {
        'success': False, 
        'error': 400,
        'errors': errors, 
      }, 400

class UserResource(Resource):
  def get(self, **kwargs):
    user_id = int(kwargs['user_id'].strip())
    user = None 
    try: 
      user = db.session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
      return abort(404)
    
    user_payload = _user_payload(user)
    user_payload['success'] = True
    return user_payload, 200

  def patch(self, **kwargs):
    user_id = int(kwargs['user_id'].strip())
    user = None 
    try: 
      user = db.session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
      return abort(404)

    proceed = True 
    errors = []
    data = json.loads(request.data)

    proceed, first_name, errors = _validate_field(data, 'first_name', proceed, errors, missing_okay=True)
    proceed, last_name, errors = _validate_field(data, 'last_name', proceed, errors, missing_okay=True)
    proceed, email, errors = _validate_field(data, 'email', proceed, errors, missing_okay=True)
    
    if not proceed: 
      return {
        'success': False, 
        'error': 400,
        'errors': errors
      }, 400
    
    if first_name and len(first_name.strip()) > 0:
      user.first_name = first_name
    if last_name and len(last_name.strip()) > 0: 
      user.last_name = last_name
    if email and len(email.strip()) > 0: 
      user.email = email 

    user.update()

    user_payload = _user_payload(user)
    user_payload['success'] = True 
    return user_payload, 200
