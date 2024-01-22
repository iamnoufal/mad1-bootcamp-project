from flask import Flask, render_template, request, session, redirect, url_for
from db import db
import os
from flask_restful import Api

app = Flask(__name__)
curr_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(curr_dir, 'db.sqlite3')}"
app.config['UPLOAD_FOLDER'] = "static"

app.secret_key = "lrkwkughoiuerhngf"

db.init_app(app)
api = Api(app)
app.app_context().push()

from models import User, Post, Follower

# db.create_all()

# user = User(username="abc", name="abc", password="abc", email="test@gmail.com", role="admin")
# db.session.add(user)
# db.session.commit()

# user = db.session.query(User).filter(User.username=="abc").first()
# if user is None:
#   print('none')
# else:
#   user.name = "ABCD"
#   db.session.commit()

# db.session.query(User).filter(User.username=="abc").delete()
# db.session.commit()

@app.route("/admin")
def adminHomePage():
  return "ADMIN"


@app.route('/')
def home():
  print(session)
  if 'username' in session:
    if session['role'] == 'admin':
      return redirect(url_for('adminHomePage'))
    else:
      return redirect(url_for('userHomePage'))
  else:
    return redirect(url_for('login'))
  
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template("login.html")
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    user = db.session.query(User).filter(User.username==username).first()
    if user is None:
      return render_template("login.html", err_msg="User not found")
    else:
      if user.password == password:
        session['username'] = user.username
        session['role'] = user.role
        if user.role == "admin": return redirect(url_for('adminHomePage'))
        else: return redirect(url_for('userHomePage'))
      else:
        return render_template("login.html", err_msg="Invalid password")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == "GET":
    return render_template("signup.html")
  else:
    username = request.form.get("username")
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    
    print(username, email, password, name)
    
    user = User(username=username, name=name, password=password, email=email)
    try:
      db.session.add(user)
      db.session.commit()
    except Exception as e:
      print(e)
      return render_template("signup.html", err_msg="User already exists")
    else:
      return redirect(url_for('login'))

from routes.post import *
from routes.user import *
from routes.search import *


from api.post import PostAPI

api.add_resource(PostAPI, '/api/post', '/api/post/<post_id>')

if __name__ == '__main__':
  app.run(port=8000, debug=True)