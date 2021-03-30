import json 
import unittest 
from copy import deepcopy

from api import create_app, db 
from api.database.models import User, Contact 
from tests import assert_payload_field_type_value, assert_payload_field_type

class CreateContactTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.user = User(email='jc@example.com', first_name='joshua', last_name='carey')
    self.user.insert()

    self.payload = {
      'first_name': 'darrel',
      'last_name': 'wadsworth', 
      'group': 'friend', 
      'phone_number': '999-999-9999',
      'street_address': '45321 example way',
      'city': 'Denver',
      'state': 'Colorado',
      'zipcode': '80000'  
    }

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_create_contact(self):
    payload = deepcopy(self.payload)

    response = self.client.post(f'/users/{self.user.id}/contacts', 
    json=payload, content_type='application/json')

    self.assertEqual(201, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'first_name', str, payload['first_name'])
    assert_payload_field_type_value(self, data, 'last_name', str, payload['last_name'])
    assert_payload_field_type_value(self, data, 'group', str, payload['group'])
    assert_payload_field_type_value(self, data, 'phone_number', str, payload['phone_number'])
    assert_payload_field_type_value(self, data, 'street_address', str, payload['street_address'])
    assert_payload_field_type_value(self, data, 'city', str, payload['city'])
    assert_payload_field_type_value(self, data, 'state', str, payload['state'])
    assert_payload_field_type_value(self, data, 'zipcode', str, payload['zipcode'])

  def test_sadpath_missing_required_field(self):
    payload = deepcopy(self.payload)
    del payload['first_name']

    response = self.client.post(f'/users/{self.user.id}/contacts', 
    json=payload, content_type='application/json')

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'first_name' parameter is missing"])

  def test_sadpath_missing_other_required_field(self):
    payload = deepcopy(self.payload)
    del payload['city']

    response = self.client.post(f'/users/{self.user.id}/contacts', 
    json=payload, content_type='application/json')

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'city' parameter is missing"])

  def test_sadpath_blank_required_field(self):
    payload = deepcopy(self.payload)
    payload['street_address'] = ''

    response = self.client.post(f'/users/{self.user.id}/contacts', 
    json=payload, content_type='application/json')

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'street_address' parameter is blank"])

  def test_sadpath_another_blank_required_field(self):
    payload = deepcopy(self.payload)
    payload['last_name'] = ''

    response = self.client.post(f'/users/{self.user.id}/contacts', 
    json=payload, content_type='application/json')

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'last_name' parameter is blank"])
