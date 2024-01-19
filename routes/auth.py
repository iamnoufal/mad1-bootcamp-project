from flask import current_app as app, render_template, request, session, redirect, url_for
from models import User
from db import db

@app.route('/')
def home():
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
