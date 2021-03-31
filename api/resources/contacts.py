import json 
from flask import request 
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api import db 
from api.database.models import User, Contact 
from . import _validate_field, _error_response

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
      contact = Contact(user, data)
      contact.insert()
        
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
      return _error_response(errors, 400)

  def get(self, **kwargs):
    user_id = int(kwargs['user_id'].strip())
    user = _validate_user(user_id)

    contacts = db.session.query(Contact).filter_by(user_id=user.id)
    contact_payload = {}
    contact_list = []

    for contact in contacts:
      contact_list.append(_contact_payload(contact))
      
    contact_payload['contacts'] = contact_list
    contact_payload['success'] = True
    
    return contact_payload, 200

class ContactResource(Resource):
  '''
  requires valid user_id and contact_id argument 
  endpoints for show, update, and delete contacts 
  [GET, PATCH, DELETE] /users/<user_id>/contacts/<contact_id>
  '''
  def _update_contact(self, contact, data):
    proceed = True 
    errors = []

    proceed, first_name, errors = _validate_field(data, 'first_name', proceed, errors, missing_okay=True)
    proceed, last_name, errors = _validate_field(data, 'last_name', proceed, errors, missing_okay=True)
    proceed, group, errors = _validate_field(data, 'group', proceed, errors, missing_okay=True)
    proceed, phone_number, errors = _validate_field(data, 'phone_number', proceed, errors, missing_okay=True)
    proceed, street_address, errors = _validate_field(data, 'street_address', proceed, errors, missing_okay=True)
    proceed, street_address_2, errors = _validate_field(data, 'street_address_2', proceed, errors, missing_okay=True)
    proceed, city, errors = _validate_field(data, 'city', proceed, errors, missing_okay=True)
    proceed, state, errors = _validate_field(data, 'state', proceed, errors, missing_okay=True)
    proceed, zipcode, errors = _validate_field(data, 'zipcode', proceed, errors, missing_okay=True)

    if proceed: 
      if first_name:
        contact.first_name = first_name
      if last_name:
        contact.last_name = last_name
      if group:
        contact.group = group
      if phone_number:
        contact.phone_number = phone_number
      if street_address:
        contact.street_address = street_address
      if street_address_2:
        contact.street_address_2 = street_address_2
      if city:
        contact.city = city
      if state:
        contact.state = state
      if zipcode:
        contact.zipcode = zipcode

      return contact, errors
    else: 
      return None, errors 

  def get(self, **kwargs):
    user_id = int(kwargs['user_id'].strip())
    user = _validate_user(user_id)

    contact_id = int(kwargs['contact_id'].strip())

    try: 
      contact = db.session.query(Contact).filter_by(id=contact_id).one()
    except: 
      errors = [f"contact with id: '{contact_id}' not found"]
      return _error_response(errors, 400)

    contact_payload = _contact_payload(contact)
    contact_payload['success'] = True

    return contact_payload, 200

  def patch(self, **kwargs):
    user_id = int(kwargs['user_id'].strip())
    user = _validate_user(user_id)

    contact_id = int(kwargs['contact_id'].strip())

    try: 
      contact = db.session.query(Contact).filter_by(id=contact_id).one()
      contact, errors = self._update_contact(contact, json.loads(request.data))
    except NoResultFound: 
      errors = [f"contact with id: '{contact_id}' not found"]
      return _error_response(errors, 400)

    if contact is not None: 
      contact_payload = _contact_payload(contact)
      contact_payload['success'] = True 

      return contact_payload, 200
    else: 
      return _error_response(errors, 400)

  def delete(self, **kwargs):
    user_id = int(kwargs['user_id'].strip())
    user = _validate_user(user_id)

    contact_id = int(kwargs['contact_id'].strip())

    try: 
      contact = db.session.query(Contact).filter_by(id=contact_id).one()
      contact.delete()
    except NoResultFound: 
      errors = [f"contact with id: '{contact_id}' not found"]
      return _error_response(errors, 400)

    return {}, 204
