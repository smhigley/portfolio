import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from config import basedir

# init app with config
app = Flask(__name__)
app.config.from_object('config')

# database with sqlalchemy
db = SQLAlchemy(app)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# init email
# mail = Mail(app)

from app import views, models

if __name__ == "__main__":
  app.run()
