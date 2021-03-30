import json 
import unittest
from copy import deepcopy

from api import create_app, db 
from api.database.models import User, Contact 
from tests import assert_payload_field_type_value, assert_payload_field_type

class UpdateContactTest(unittest.TestCase):
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

    self.update_payload = {
      'first_name': 'bruce',
      'last_name': 'wayne', 
      'group': 'associate', 
      'phone_number': '111-111-1111',
      'street_address': 'the bat cave',
      'city': 'Pagosa Springs',
      'state': 'Colorado',
      'zipcode': '12345'  
    }

    self.contact = Contact(self.user, self.contact_payload)
    self.contact.insert()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_update_contact(self):
    payload = deepcopy(self.update_payload)

    response = self.client.patch(f'/users/{self.user.id}/contacts/{self.contact.id}',
    json=payload, content_type='application/json')

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'first_name', str, self.update_payload['first_name'])
    assert_payload_field_type_value(self, data, 'last_name', str, self.update_payload['last_name'])
    assert_payload_field_type_value(self, data, 'group', str, self.update_payload['group'])
    assert_payload_field_type_value(self, data, 'phone_number', str, self.update_payload['phone_number'])
    assert_payload_field_type_value(self, data, 'street_address', str, self.update_payload['street_address'])
    assert_payload_field_type_value(self, data, 'city', str, self.update_payload['city'])
    assert_payload_field_type_value(self, data, 'state', str, self.update_payload['state'])
    assert_payload_field_type_value(self, data, 'zipcode', str, self.update_payload['zipcode'])

  def test_sadpath_blank_required_field(self):
    payload = deepcopy(self.update_payload)
    payload['first_name'] = ''

    response = self.client.patch(f'/users/{self.user.id}/contacts/{self.contact.id}',
    json=payload, content_type='application/json')

    self.assertEqual(400, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'first_name' parameter is blank"])

  def test_sadpath_another_blank_required_field(self):
    payload = deepcopy(self.update_payload)
    payload['street_address'] = ''

    response = self.client.patch(f'/users/{self.user.id}/contacts/{self.contact.id}',
    json=payload, content_type='application/json')

    self.assertEqual(400, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'street_address' parameter is blank"])

  def test_sadpath_update_contact_with_only_one_field(self):
    payload = deepcopy(self.update_payload)

    # only update street address
    del payload['first_name']
    del payload['last_name']
    del payload['group']
    del payload['phone_number']
    del payload['city']
    del payload['state']
    del payload['zipcode']

    response = self.client.patch(f'/users/{self.user.id}/contacts/{self.contact.id}',
    json=payload, content_type='application/json')

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))

    # only street address should match with update_payload
    assert_payload_field_type_value(self, data, 'street_address', str, self.update_payload['street_address'])

    # everything else should match the original payload
    assert_payload_field_type_value(self, data, 'first_name', str, self.contact_payload['first_name'])
    assert_payload_field_type_value(self, data, 'last_name', str, self.contact_payload['last_name'])
    assert_payload_field_type_value(self, data, 'group', str, self.contact_payload['group'])
    assert_payload_field_type_value(self, data, 'phone_number', str, self.contact_payload['phone_number'])
    assert_payload_field_type_value(self, data, 'city', str, self.contact_payload['city'])
    assert_payload_field_type_value(self, data, 'state', str, self.contact_payload['state'])
    assert_payload_field_type_value(self, data, 'zipcode', str, self.contact_payload['zipcode'])

  def test_sadpath_invalid_user_id(self):
    payload = deepcopy(self.update_payload)

    response = self.client.patch(f'/users/99999/contacts/{self.contact.id}',
    json=payload, content_type='application/json')

    self.assertEqual(404, response.status_code)

  def test_sadpath_invalid_contact_id(self):
    payload = deepcopy(self.update_payload)
    contact_id = 99999

    response = self.client.patch(f'/users/{self.user.id}/contacts/{contact_id}',
    json=payload, content_type='application/json')

    self.assertEqual(400, response.status_code)
    
    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, [f"contact with id: '{contact_id}' not found"])
