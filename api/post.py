from flask_restful import fields, reqparse, Resource, marshal_with
from db import db
from models import Post

post_input_fields = reqparse.RequestParser()
post_input_fields.add_argument('title')
post_input_fields.add_argument('description')
post_input_fields.add_argument('image')
post_input_fields.add_argument("created_by")

post_output_fields = {
  "id": fields.Integer,
  "title": fields.String,
  "description": fields.String,
  "image_url": fields.String,
  "created_by": fields.String
}

class PostAPI(Resource):

  @marshal_with(post_output_fields)
  def get(self, post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first()
    return post

  def post(self):
    args = post_input_fields.parse_args()
    title = args.get("title")
    description = args.get('description')
    created_by = args.get("created_by")
    post = Post(title=title, description=description, created_by=created_by)
    try:
      db.session.add(post)
      db.session.commit()
    except Exception as e:
      print(e)
      return e
    else:
      return "Success"

  def put(self, post_id):
    post = db.session.query(Post).filter(Post.id==post_id).first()
    args = post_input_fields.parse_args()
    post.title = args.get("title")
    post.description = args.get('description')
    
    try:
      db.session.commit()
    except Exception as e:
      print(e)
      return e
    else:
      return "success"

  def delete(self, post_id):
    print(post_id)
    db.session.query(Post).filter(Post.id==post_id).delete()
    db.session.commit()
    print("deleted")
    return "delete"