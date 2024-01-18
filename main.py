from flask import Flask
from db import db
import os

app = Flask(__name__)
curr_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(curr_dir, 'db.sqlite3')}"

db.init_app(app)
app.app_context().push()

from models import User

db.create_all()

# user = User(username="abc", name="abc", password="abc", email="test@gmail.com", role="admin")
# db.session.add(user)
# db.session.commit()

# user = db.session.query(User).filter(User.username=="abc").first()
# if user is None:
#   print('none')
# else:
#   user.name = "ABCD"
#   db.session.commit()

db.session.query(User).filter(User.username=="abc").delete()
db.session.commit()

# if __name__ == '__main__':
#   app.run()