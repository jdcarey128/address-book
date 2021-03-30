import json 
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

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

  return proceed, data[field], errors


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
      return {
        'success': True,
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
      }, 201
    else: 
      return {
        'success': False, 
        'error': 400,
        'errors': errors, 
      }, 400
