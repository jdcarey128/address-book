import json 
import unittest 

from api import create_app, db
from api.database.models import User 

class DeleteUserTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.user = User(email='jc@example.com', first_name='joshua', last_name='carey')
    self.user.insert()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_happypath_user_delete(self):
    user = self.user 
    response = self.client.delete(f'/users/{self.user.id}')
    self.assertEqual(204, response.status_code)

    response = self.client.get(
      f'/users/{user.id}'
    )
    self.assertEqual(404, response.status_code)

  def test_sadpath_user_delete_invalid_id(self):
    response = self.client.delete(f'/users/9999')
    self.assertEqual(404, response.status_code)
