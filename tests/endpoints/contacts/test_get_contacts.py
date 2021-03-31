import json 
import unittest 
from copy import deepcopy

from api import create_app, db 
from api.database.models import User, Contact 
from tests import assert_payload_field_type_value, assert_payload_field_type

class GetContactsTest(unittest.TestCase):
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

    # creates three contacts (all attributes differentiated by '_i') for user 
    # TODO: good use case for factory bot 

    for i in range(3):
      payload = deepcopy(self.contact_payload)
      for key, value in payload.items():
        payload[key] = value + f'_{i}' 
      Contact(self.user, payload)

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_show_contacts(self):
    payload = deepcopy(self.contact_payload)

    response = self.client.get(f'/users/{self.user.id}/contacts')

    self.assertEqual(200, response.status_code)
    data = json.loads(response.data.decode('utf-8'))


    assert_payload_field_type_value(self, data, 'success', bool, True)
    assert_payload_field_type(self, data, 'contacts', list)

    self.assertEqual(3, len(data['contacts']))
    
    contacts = data['contacts']
    for contact in contacts: 
      assert_payload_field_type(self, contact, 'first_name', str)
      assert_payload_field_type(self, contact, 'last_name', str)
      assert_payload_field_type(self, contact, 'group', str)
      assert_payload_field_type(self, contact, 'phone_number', str)
      assert_payload_field_type(self, contact, 'street_address', str)
      assert_payload_field_type(self, contact, 'city', str)
      assert_payload_field_type(self, contact, 'state', str)
      assert_payload_field_type(self, contact, 'zipcode', str)
  
  def test_sad_path_user_has_zero_contacts(self):
    user = User(email='example@example.com', first_name='example', last_name='fake')
    user.insert()

    response = self.client.get(f'/users/{user.id}/contacts')

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, True)
    assert_payload_field_type(self, data, 'contacts', list)
    self.assertEqual(0, len(data['contacts']))

  def test_sad_path_user_id_invalid(self):
    response = self.client.get(f'/users/99999/contacts')

    self.assertEqual(404, response.status_code)
