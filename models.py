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
  role = db.Column(db.String, default="user")
  posts = db.relationship('Post', backref='users')

class Post(db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String)
  description = db.Column(db.String)
  image_url = db.Column(db.String)
  created_by = db.Column(db.String, db.ForeignKey('users.username'))