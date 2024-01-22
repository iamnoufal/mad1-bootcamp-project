from flask import current_app as app, render_template, session, redirect, url_for
from db import db
from models import Post, User, Follower

@app.route("/admin")
def adminHomePage():
  posts = db.session.query(Post).all()
  return render_template("admin_home.html")