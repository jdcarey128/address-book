import json 
import unittest 

from api.database.models import User 
from api import create_app, db 
from tests import assert_payload_field_type_value, assert_payload_field_type

class ShowUserTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.user_1 = User(email="jpwizard", first_name="james", last_name="potter")
    self.user_1.insert()

    self.user_2 = User(email="example@example.com", first_name="hiawatha", last_name="francisco")
    self.user_2.insert()
     
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_show_user(self):
    response = self.client.get(
      f'/users/{self.user_1.id}'
    )

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    assert_payload_field_type_value(self, data, 'success', bool, True)
    assert_payload_field_type_value(self, data, 'first_name', str, self.user_1.first_name)
    assert_payload_field_type_value(self, data, 'last_name', str, self.user_1.last_name)
    assert_payload_field_type_value(self, data, 'email', str, self.user_1.email)

  def test_invalid_user_id(self):
    response = self.client.get(
      '/users/9999'
    )

    error_message = 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'

    data = json.loads(response.data.decode('utf-8'))

    self.assertEqual(404, response.status_code)
    assert_payload_field_type_value(self, data, 'message', str, error_message)
