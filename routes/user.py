from flask import current_app as app, render_template, session, redirect, url_for
from db import db
from models import Post, User, Follower

@app.route("/user")
def userHomePage():
  posts = db.session.query(Post).all()
  return render_template("user_home.html", posts = posts, session = session)

@app.route("/user/profile")
def userProfile():
  user = db.session.query(User).filter(User.username == session['username']).first()
  return render_template("profile.html", user=user)

@app.route("/user/<username>")
def otherUserProfile(username):
  user = db.session.query(User).filter(User.username == username).first()
  return render_template("profile.html", user=user, session = session, followers = [u.from_id for u in user.followers])

@app.route('/user/<username>/follow')
def userFollow(username):
  following = Follower(from_id = session['username'], to_id = username)
  db.session.add(following)
  db.session.commit()
  return redirect(url_for('otherUserProfile', username=username))

@app.route('/user/<username>/unfollow')
def userUnfollow(username):
  db.session.query(Follower).filter(Follower.from_id == session['username'], Follower.to_id == username).delete()
  db.session.commit()
  return redirect(url_for('otherUserProfile', username=username))