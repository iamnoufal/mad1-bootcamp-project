from flask import current_app as app, render_template, session
from db import db
from models import Post, User

@app.route("/user")
def userHomePage():
  posts = db.session.query(Post).all()
  return render_template("user_home.html", posts = posts, session = session)

@app.route("/user/profile")
def userProfile():
  user = db.session.query(User).filter(User.username == session['username']).first()
  return render_template("profile.html", user=user)