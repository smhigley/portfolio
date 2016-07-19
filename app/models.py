from werkzeug.security import generate_password_hash, \
     check_password_hash
from app import db

class User(db.Model):
  id = db.Column(db.String(64), primary_key=True) # use username as id
  password = db.Column(db.String(64))
  email = db.Column(db.String(120), unique=True)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    try:
      return unicode(self.id)  # python 2
    except NameError:
      return str(self.id)  # python 3

  def __repr__(self):
    return '<User %r>' % (self.id)


class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64))
  slug = db.Column(db.String(32), unique=True, index=True)
  image = db.Column(db.String(64))
  link = db.Column(db.String(64))
  body = db.Column(db.String(140))
  client = db.Column(db.String(32))
  featured = db.Column(db.Boolean)
  timestamp = db.Column(db.DateTime)

  def __repr__(self):
    return '<Project %r>' % (self.title)


class Page(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64))
  slug = db.Column(db.String(32), unique=True, index=True)
  body = db.Column(db.String(140))

  def __repr__(self):
    return '<Page %r>' % (self.title)
