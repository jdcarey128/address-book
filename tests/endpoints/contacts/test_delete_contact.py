import json 
import unittest
from copy import deepcopy

from api import create_app, db 
from api.database.models import User, Contact 
from tests import assert_payload_field_type_value, assert_payload_field_type

class DeleteContactTest(unittest.TestCase):
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

  def test_happypath_delete_contact(self):
    response = self.client.delete(f'/users/{self.user.id}/contacts/{self.contact.id}')

    self.assertEqual(204, response.status_code)

    response = self.client.delete(f'/users/{self.user.id}/contacts/{self.contact.id}')

    self.assertEqual(400, response.status_code)

  def test_sadpath_delete_test_invalide_contact_id(self):
    contact_id = 9999
    
    response = self.client.delete(f'/users/{self.user.id}/contacts/{contact_id}')

    self.assertEqual(400, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, [f"contact with id: '{contact_id}' not found"])

  def test_sadpath_delete_test_invalid_user_id(self):
    response = self.client.delete(f'/users/99999/contacts/{self.contact.id}')

    self.assertEqual(404, response.status_code)
