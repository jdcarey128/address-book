import json 
import unittest 
from copy import deepcopy

from api.database.models import User 
from api import create_app, db 
from tests import assert_payload_field_type, assert_payload_field_type_value

class LoginUserTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client() 

    self.user_1 = User(email="jpwizard", first_name="james", last_name="potter")
    self.user_1.insert()

    self.payload = {
      'email': 'jpwizard'
    }

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_login_user(self): 
    payload = deepcopy(self.payload)

    response = self.client.post(
      '/login', json=payload,
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, True)
    assert_payload_field_type_value(self, data, 'id', int, self.user_1.id)
    assert_payload_field_type_value(self, data, 'first_name', str, self.user_1.first_name)
    assert_payload_field_type_value(self, data, 'last_name', str, self.user_1.last_name)
    assert_payload_field_type_value(self, data, 'email', str, self.user_1.email)

  def test_sadpath_email_not_found(self):
    payload = deepcopy(self.payload)
    payload['email'] = 'email_not_found@example.com'

    response = self.client.post(
      '/login', json=payload,
      content_type='application/json'
    )

    self.assertEqual(404, response.status_code)

  def test_sadpath_email_is_blank(self):
    payload = deepcopy(self.payload)
    payload['email'] = ''

    response = self.client.post(
      '/login', json=payload,
      content_type='application/json'
    )

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'email' parameter is blank"])

  def test_sadpath_email_is_missing(self):
    payload = deepcopy(self.payload)
    del payload['email']

    response = self.client.post(
      '/login', json=payload,
      content_type='application/json'
    )

    self.assertEqual(400, response.status_code)
    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, False)
    assert_payload_field_type_value(self, data, 'error', int, 400)
    assert_payload_field_type_value(self, data, 'errors', list, ["required 'email' parameter is missing"])
