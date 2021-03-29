import unittest 
from sqlalchemy.exc import IntegrityError

from api import create_app, db 
from api.database.models import User 

class UserTest(unittest.TestCase):
  def setUp(self): 
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_user_model(self):
    user = User(email = 'joshua@example.com', 
                first_name = 'joshua',
                last_name = 'carey',
                )
    user.insert()

    self.assertIsInstance(user, User)
    self.assertIsNotNone(user.id)
    self.assertEqual('joshua', user.first_name)
    self.assertEqual('carey', user.last_name)
    self.assertEqual('joshua@example.com', user.email)

  def test_user_model_missing_first_name(self):
    try: 
      user = User(email = 'joshua@example.com', 
                  first_name = None,
                  last_name = 'carey',
                  )
      user.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      # should not end here 
      self.assertTrue(False) 

  def test_user_model_missing_last_name(self):
    try: 
      user = User(email = 'joshua@example.com', 
                  first_name = 'joshua',
                  last_name = None,
                  )
      user.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      # should not end here 
      self.assertTrue(False) 

  def test_user_model_missing_email(self):
    try: 
      user = User(email = None, 
                  first_name = 'joshua',
                  last_name = 'carey',
                  )
      user.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      # should not end here 
      self.assertTrue(False) 

  def test_user_model_unique_email(self):
    user = User(email = 'joshua@example.com', 
                first_name = 'joshua',
                last_name = 'carey',
                )
    user.insert()

    try: 
      user = User(email = 'joshua@example.com', 
                  first_name = 'joshua',
                  last_name = 'carey',
                  )
      user.insert()
    except IntegrityError:
      self.assertTrue(True)
    else:
      # should not end here 
      self.assertTrue(False)

  def test_user_model_trims_space(self):
    user = User(email = '   joshua@example.com ', 
                  first_name = '  joshua  ',
                  last_name = '  carey  ',
                  )
    user.insert()

    self.assertEqual('joshua', user.first_name)
    self.assertEqual('carey', user.last_name)
    self.assertEqual('joshua@example.com', user.email)

  def test_user_model_blank_email(self):
    try: 
      user = User(email = '', 
                  first_name = 'joshua',
                  last_name = 'carey',
                  )
      user.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      # should not end here
      self.assertTrue(False)

  def test_user_model_blank_first_name(self):
    try: 
      user = User(email = 'joshua@example.com', 
                  first_name = '',
                  last_name = 'carey',
                  )
      user.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      # should not end here
      self.assertTrue(False)

  def test_user_model_blank_last_name(self):
    try: 
      user = User(email = 'joshua@example.com', 
                  first_name = 'joshua',
                  last_name = '',
                  )
      user.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      # should not end here
      self.assertTrue(False)
