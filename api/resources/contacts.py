import json 
from flask import request 
from flask_restful import Resource, abort 
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api import db 
from api.database.models import User, Contact 
from . import _validate_field, _error_400

def _validate_user(user_id):
  try: 
    user = db.session.query(User).filter_by(id=user_id).one() 
  except NoResultFound: 
    return abort(404)
    
  return user

def _contact_payload(contact):
  return {
    'first_name': contact.first_name,
    'last_name': contact.last_name,
    'group': contact.group,
    'phone_number': contact.phone_number,
    'street_address': contact.street_address,
    'street_address_2': contact.street_address_2,
    'city': contact.city,
    'state': contact.state,
    'zipcode': contact.zipcode,
  }

class ContactsResource(Resource):
  '''
  requires a valid user_id argument 
  get and create contact [GET, POST] /users/<user_id>/contacts
  '''
  def _create_contact(self, user, data):
    proceed = True 
    errors = []
    
    proceed, first_name, errors = _validate_field(data, 'first_name', proceed, errors)
    proceed, last_name, errors = _validate_field(data, 'last_name', proceed, errors)
    proceed, group, errors = _validate_field(data, 'group', proceed, errors, missing_okay=True)
    proceed, phone_number, errors = _validate_field(data, 'phone_number', proceed, errors, missing_okay=True)
    proceed, street_address, errors = _validate_field(data, 'street_address', proceed, errors)
    proceed, street_address_2, errors = _validate_field(data, 'street_address_2', proceed, errors, missing_okay=True)
    proceed, city, errors = _validate_field(data, 'city', proceed, errors)
    proceed, state, errors = _validate_field(data, 'state', proceed, errors)
    proceed, zipcode, errors = _validate_field(data, 'zipcode', proceed, errors)

    if proceed: 
      try: 
        contact = Contact(user, data)
        contact.insert()
      except:
        contact = None 
        import ipdb; ipdb.set_trace(context=5)
        
      return contact, errors
    else: 
      return None, errors

  def post(self, **kwargs):
    user_id = int(kwargs['user_id'].strip())
    user = _validate_user(user_id)

    contact, errors = self._create_contact(user, json.loads(request.data))

    if contact is not None:
      contact_payload = _contact_payload(contact)
      contact_payload['success'] = True 
      return contact_payload, 201
    else: 
      return _error_400(errors)

class ContactResource(Resource):
  '''
  requires valid user_id and contact_id argument 
  endpoints for show, update, and delete contacts 
  [GET, PATCH, DELETE] /users/<user_id>/contacts/<contact_id>
  '''
