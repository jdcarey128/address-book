import json 
import unittest 
from copy import deepcopy

from api import create_app, db
from api.database.models import User 
from tests import assert_payload_field_type_value, assert_payload_field_type

class UpdateUserTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.user = User(email='jc@example.com', first_name='joshua', last_name='carey')
    self.user.insert()

    self.payload = {
      'first_name': 'jonathan',
      'last_name': 'bridges',
      'email': 'jbridges@example.com'
    }

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_update_user(self):
    payload = deepcopy(self.payload)
    
    response = self.client.patch(
      f'/users/{self.user.id}', json=payload, 
      content_type='application/json'
    )
    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, True)
    assert_payload_field_type_value(self, data, 'first_name', str, self.payload['first_name'])
    assert_payload_field_type_value(self, data, 'last_name', str, self.payload['last_name'])
    assert_payload_field_type_value(self, data, 'email', str, self.payload['email'])

  def test_happypath_update_user_with_only_email(self):
    payload = deepcopy(self.payload)
    del payload['first_name']
    del payload['last_name']

    response = self.client.patch(
      f'/users/{self.user.id}', json=payload, 
      content_type='application/json'
    )
    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, True)
    assert_payload_field_type_value(self, data, 'first_name', str, self.user.first_name)
    assert_payload_field_type_value(self, data, 'last_name', str, self.user.last_name)
    assert_payload_field_type_value(self, data, 'email', str, self.payload['email'])

  def test_sadpath_first_name_blank(self):
    payload = deepcopy(self.payload)
    payload['first_name'] = ''

    response = self.client.patch(
      f'/users/{self.user.id}', json=payload,
      content_type='application/json'
    )

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'first_name' parameter is blank"])

  def test_sadpath_last_name_blank(self):
    payload = deepcopy(self.payload)
    payload['last_name'] = ''

    response = self.client.patch(
      f'/users/{self.user.id}', json=payload,
      content_type='application/json'
    )

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'last_name' parameter is blank"])

  def test_sadpath_email_blank(self):
    payload = deepcopy(self.payload)
    payload['email'] = ''

    response = self.client.patch(
      f'/users/{self.user.id}', json=payload,
      content_type='application/json'
    )

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'email' parameter is blank"])

  def test_sadpath_invalid_user_id(self):
    payload = deepcopy(self.payload)

    response = self.client.patch(
      '/users/9999', json=payload,
      content_type='application/json'
    )
    self.assertEqual(404, response.status_code)
