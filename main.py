from flask import Flask, render_template, request
from db import db
import os

app = Flask(__name__)
curr_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(curr_dir, 'db.sqlite3')}"

db.init_app(app)
app.app_context().push()

from models import User

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

# http://127.0.0.1:8000/

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template("login.html")
  else:
    return "POST"

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
    db.session.add(user)
    db.session.commit()
    # print(username)
    return "POST"

if __name__ == '__main__':
  app.run(port=8000, debug=True)