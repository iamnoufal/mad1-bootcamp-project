from flask import current_app as app, request, render_template
from db import db
from models import User

@app.route("/user/search", methods=['GET', 'POST'])
def search():
  if request.method == "GET":
    return render_template("search.html")
  else:
    query = request.form.get("query")
    users = db.session.query(User).filter(User.name.like(f"%{query}%")).all()
    return render_template("search.html", users = users)