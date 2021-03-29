import unittest 
from sqlalchemy.exc import IntegrityError

from api import create_app, db 
from api.database.models import User, Contact

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

  def test_user_model_can_update(self):
    user = User (
                email = 'joshua@example.com', 
                first_name = 'joshua',
                last_name = 'carey',
                )
    user.insert()

    user.email = 'jc@example.com'
    user.update()

    updated_user = User.query.filter_by(id = user.id).first()

    self.assertEqual('jc@example.com', updated_user.email)

  def test_user_model_can_delete_record(self):
    user = User(email = 'joshua@example.com', 
                first_name = 'joshua',
                last_name = 'carey',
                )
    user.insert()
    user.delete()

    deleted_user = User.query.filter_by(id=user.id).first()

    self.assertIsNone(deleted_user)

  def test_user_model_can_delete_record_and_its_contacts(self):
    user = User(email = 'joshua@example.com', 
                first_name = 'joshua',
                last_name = 'carey',
                )
    user.insert()
    self.assertEqual([], user.contacts)

    contact = Contact(user, {
              'first_name': 'emilio',
              'last_name': 'estevez',
              'group': 'business',
              'phone_number': '999-999-9999',
              'street_address': '1234 fake st',
              'street_address_2': 'unit 100',
              'city': 'denver',
              'state': 'colorado',
              'zipcode': '80019'
              })
    contact.insert()

    self.assertEqual([contact], user.contacts)

    user.delete()
    deleted_user = User.query.filter_by(id=user.id).first()
    self.assertIsNone(deleted_user)
    deleted_contact = Contact.query.filter_by(id=user.id).first()
    self.assertIsNone(deleted_contact)
