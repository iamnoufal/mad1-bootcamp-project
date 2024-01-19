from flask import current_app as app, flash, request, redirect, render_template, url_for, send_from_directory, session
from models import Post
from db import db
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
  if request.method == "GET":
    return render_template("create_post.html")
  else:
    title = request.form.get("title")
    description = request.form.get('description')
    image = request.files['image']
    
    if image and allowed_file(image.filename):
      filename = secure_filename(image.filename)
      image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      image_url = url_for('uploaded_file', filename=filename)

    post = Post(title=title, description=description, image_url=image_url, created_by=session['username'])
    try:
      db.session.add(post)
      db.session.commit()
    except Exception as e:
      print(e)
      flash("Something went wrong")
    else:
      return redirect(url_for('home'))

@app.route('/post/<post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
  post = db.session.query(Post).filter(Post.id==post_id).first()
  if post is None:
    return "Post not found"

  if request.method == "GET":
    return render_template("edit_post.html", post = post)
  else:
    post.title = request.form.get("title")
    post.description = request.form.get('description')
    image = request.files['image']
    
    if image and allowed_file(image.filename):
      filename = secure_filename(image.filename)
      image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      post.image_url = url_for('uploaded_file', filename=filename)
    try:
      db.session.commit()
    except Exception as e:
      print(e)
      flash("Something went wrong")
    else:
      return redirect(url_for('home'))

@app.route('/post/<post_id>/delete')
def delete_post(post_id):
  print(post_id)
  db.session.query(Post).filter(Post.id==post_id).delete()
  print("deleted")
  return redirect(url_for('home'))