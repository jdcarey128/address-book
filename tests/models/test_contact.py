import unittest 
from sqlalchemy.exc import IntegrityError

from api import create_app, db 
from api.database.models import User, Contact 

class ContactTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.user = User(email = 'joshua@example.com', 
                first_name = 'joshua',
                last_name = 'carey',
                )
    self.user.insert()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
  def test_contact_model(self):
    contact = Contact(self.user, 
                      {'first_name': 'emilio',
                      'last_name': 'estevez',
                      'street_address': '1234 fake st',
                      'city': 'denver',
                      'state': 'colorado',
                      'zipcode': '80019'
                      })
    contact.insert()

    self.assertIsInstance(contact, Contact)
    self.assertIsNotNone(contact.id)
    self.assertIsNotNone(contact.user_id)
    self.assertEqual(self.user, contact.user)
    self.assertEqual('emilio', contact.first_name)
    self.assertEqual('estevez', contact.last_name)
    self.assertEqual('1234 fake st', contact.street_address)
    self.assertEqual('denver', contact.city)
    self.assertEqual('colorado', contact.state)
    self.assertEqual('80019', contact.zipcode)
    self.assertEqual('friend', contact.group)
    self.assertEqual(None, contact.street_address_2)
    self.assertEqual(None, contact.phone_number)

  def test_contact_model_with_non_required_atts(self):
    contact = Contact(self.user, 
                      {'first_name': 'emilio',
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

    self.assertEqual('business', contact.group)
    self.assertEqual('unit 100', contact.street_address_2)
    self.assertEqual('999-999-9999', contact.phone_number)

  def test_contact_model_missing_first_name(self):
    try:
      contact = Contact(self.user, 
                        {'first_name': None,
                        'last_name': 'estevez',
                        'street_address': '1234 fake st',
                        'city': 'denver',
                        'state': 'colorado',
                        'zipcode': '80019'
                        })
      contact.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      self.assertTrue(False)

  def test_contact_model_missing_last_name(self):
    try:
      contact = Contact(self.user, 
                        {'first_name': 'emilio',
                        'last_name': None,
                        'street_address': '1234 fake st',
                        'city': 'denver',
                        'state': 'colorado',
                        'zipcode': '80019'
                        })
      contact.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      self.assertTrue(False)
      
  def test_contact_model_missing_street_address(self):
    try:
      contact = Contact(self.user, 
                        {'first_name': 'emilio',
                        'last_name': 'estevez',
                        'street_address': None,
                        'city': 'denver',
                        'state': 'colorado',
                        'zipcode': '80019'
                        })
      contact.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      self.assertTrue(False)

  def test_contact_model_missing_city(self):
    try:
      contact = Contact(self.user, 
                        {'first_name': 'emilio',
                        'last_name': 'estevez',
                        'street_address': '1234 fake st',
                        'city': None,
                        'state': 'colorado',
                        'zipcode': '80019'
                        })
      contact.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      self.assertTrue(False)

  def test_contact_model_missing_state(self):
    try:
      contact = Contact(self.user, 
                        {'first_name': 'emilio',
                        'last_name': 'estevez',
                        'street_address': '1234 fake st',
                        'city': 'denver',
                        'state': None,
                        'zipcode': '80019'
                        })
      contact.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      self.assertTrue(False)

  def test_contact_model_missing_zipcode(self):
    try:
      contact = Contact(self.user, 
                        {'first_name': 'emilio',
                        'last_name': 'estevez',
                        'street_address': '1234 fake st',
                        'city': 'denver',
                        'state': 'colorado',
                        'zipcode': None
                        })
      contact.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      self.assertTrue(False)

  def test_contact_model_empty_first_name(self):
    try:
      contact = Contact(self.user, 
                        {'first_name': '',
                        'last_name': 'estevez',
                        'street_address': '1234 fake st',
                        'city': 'denver',
                        'state': 'colorado',
                        'zipcode': '99999'
                        })
      contact.insert()
    except IntegrityError:
      self.assertTrue(True)
    else: 
      self.assertTrue(False)

  def test_contact_model_can_update(self):
    contact = Contact(self.user, 
                      {'first_name': 'emilio',
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

    contact.first_name = 'harvey'
    contact.last_name = 'dent'
    contact.street_address_2 = '444 avenue way'
    contact.update()

    updated_contact = Contact.query.filter_by(id = contact.id).first()

    self.assertEqual('harvey', updated_contact.first_name)
    self.assertEqual('dent', updated_contact.last_name)
    self.assertEqual('444 avenue way', updated_contact.street_address_2)

  def test_contact_model_can_delete_record(self):
    contact = Contact(self.user, 
                      {'first_name': 'emilio',
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
    contact.delete()

    deleted_contact = Contact.query.filter_by(id = contact.id).first()

    self.assertIsNone(deleted_contact)
