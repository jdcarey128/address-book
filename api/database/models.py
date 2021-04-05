from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
# from sqlalchemy.ext.declarative import declarative_base
from api import db 
import datetime 

class User(db.Model): 
  '''
  User Model
  '''
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  email = Column(String(120), unique=True, nullable=False)
  first_name = Column(String(80), nullable=False)
  last_name = Column(String(80), nullable=False)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, 
                      default=datetime.datetime.utcnow, 
                      onupdate=datetime.datetime.utcnow)
  contacts = relationship('Contact', back_populates='user', cascade='all,delete')

  def __init__(self, email, first_name, last_name):
    if email is not None: 
      email = email.strip()
      if email == '':
        email = None
    
    if first_name is not None: 
      first_name = first_name.strip()
      if first_name == '':
        first_name = None

    if last_name is not None: 
      last_name = last_name.strip()
      if last_name == '':
        last_name = None
        
    self.email = email
    self.first_name = first_name 
    self.last_name = last_name

  def __repr__(self):
    return '<User %r>' % self.email

  def insert(self): 
    '''
    inserts new record into db with unique email
    '''
    db.session.add(self)
    db.session.commit()

  def update(self): 
    '''
    updates record that exists in db
    '''
    db.session.commit()

  def delete(self): 
    '''
    deletes record from db
    '''
    db.session.delete(self)
    db.session.commit()

class Contact(db.Model): 
  '''
  Contact Model
  '''

  __tablename__ = 'contacts'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.id'))
  first_name = Column(String(80), nullable=False)
  last_name = Column(String(80), nullable=False)
  group = Column(String(80), default='friend')
  phone_number = Column(String(80), nullable=True)
  street_address = Column(String(120), nullable=False)
  street_address_2 = Column(String(80), nullable=True)
  city = Column(String(80), nullable=False)
  state = Column(String(80), nullable=False)
  zipcode = Column(String(80), nullable=False)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, 
                      default=datetime.datetime.utcnow, 
                      onupdate=datetime.datetime.utcnow)
  user = relationship('User', back_populates='contacts')

  def __init__(self, user, details):
    self.user = user

    # loops through details dictionary and assigns nonemtpy and nonNone values to coresponding instance variable 
    for key, value, in details.items():
      if hasattr(self, key):
        if value != '' and value is not None:
          value = value.strip()
          setattr(self, key, value)
        else: 
          setattr(self, key, None)

  def insert(self): 
    '''
    inserts new record into db
    '''
    db.session.add(self)
    db.session.commit()
  
  def update(self): 
    '''
    updates record that exists in db
    '''
    db.session.commit()

  def delete(self): 
    '''
    deletes record from db
    '''
    db.session.delete(self)
    db.session.commit()

  def __repr(self): 
    return '<Contact %r>' % self.first_name + '-' + self.last_name
