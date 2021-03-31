import json 
import unittest
from copy import deepcopy

from api import create_app, db 
from api.database.models import User, Contact 
from tests import assert_payload_field_type_value, assert_payload_field_type

class ShowContactTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.user = User(email='jc@example.com', first_name='joshua', last_name='carey')
    self.user.insert()

    self.contact_payload = {
      'first_name': 'darrel',
      'last_name': 'wadsworth', 
      'group': 'friend', 
      'phone_number': '999-999-9999',
      'street_address': '45321 example way',
      'city': 'Denver',
      'state': 'Colorado',
      'zipcode': '80000'  
    }

    self.contact = Contact(self.user, self.contact_payload)
    self.contact.insert()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_get_contact(self):
    response = self.client.get(f'/users/{self.user.id}/contacts/{self.contact.id}')

    self.assertEqual(200, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, True)    
    assert_payload_field_type_value(self, data, 'first_name', str, self.contact_payload['first_name'])    
    assert_payload_field_type_value(self, data, 'last_name', str, self.contact_payload['last_name'])    
    assert_payload_field_type_value(self, data, 'group', str, self.contact_payload['group'])    
    assert_payload_field_type_value(self, data, 'phone_number', str, self.contact_payload['phone_number'])    
    assert_payload_field_type_value(self, data, 'street_address', str, self.contact_payload['street_address'])    
    assert_payload_field_type_value(self, data, 'city', str, self.contact_payload['city'])    
    assert_payload_field_type_value(self, data, 'state', str, self.contact_payload['state'])    
    assert_payload_field_type_value(self, data, 'zipcode', str, self.contact_payload['zipcode'])    

  def test_sadpath_invalid_contact_id(self):
    contact_id = 99999
    response = self.client.get(f'/users/{self.user.id}/contacts/{contact_id}')

    self.assertEqual(400, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, False)    
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, [f"contact with id: '{contact_id}' not found"])

  def test_sadpath_invalid_user_id(self):
    response = self.client.get(f'/users/99999/contacts/{self.contact.id}')

    self.assertEqual(404, response.status_code)
