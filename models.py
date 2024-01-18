from db import db

"""
user:
- username - primary key
- name
- password
- email - unique
- role - admin, user
"""
class User(db.Model):
  __tablename__ = 'users'
  username = db.Column(db.String, primary_key=True)
  name = db.Column(db.String)
  password = db.Column(db.String)
  email = db.Column(db.String, unique=True)
  role = db.Column(db.String)