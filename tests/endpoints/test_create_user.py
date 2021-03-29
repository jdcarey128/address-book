import json
import unittest
from copy import deepcopy

from api import create_app, db 
from tests import assert_payload_field_type_value, assert_payload_field_type

class CreateUserTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.payload = {
      'first_name': 'james',
      'last_name': 'potter',
      'email': 'jp@wizard.com'
    }

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_create_user(self):
    payload = deepcopy(self.payload)

    response = self.client.post(
      '/users', json=payload,
      content_type='application/json'
    )
    self.assertEqual(201, response.status_code)

    data = json.loads(response.data.decode('utf-8'))

    assert_payload_field_type_value(self, data, 'success', bool, True)
    assert_payload_field_type(self, data, 'id', int)
    assert_payload_field_type_value(self, data, 'first_name', str, payload['first_name'])
    assert_payload_field_type_value(self, data, 'last_name', str, payload['last_name'])
    assert_payload_field_type_value(self, data, 'email', str, payload['email'])
