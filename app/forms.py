from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, RadioField, BooleanField, PasswordField, validators

class LoginForm(Form):
  username = StringField('username', validators=[validators.DataRequired()])
  password = PasswordField('password', validators=[validators.DataRequired()])

class PageForm(Form):
  title = StringField('title', validators=[validators.DataRequired()])
  slug = StringField('slug', validators=[validators.DataRequired(), validators.Regexp('[\w-]+$', message="The slug must contain only letters, numbers, and dashes")])
  body = TextAreaField('body', validators=[validators.DataRequired()])

class ProjectForm(Form):
  title = StringField('title', validators=[validators.DataRequired()])
  slug = StringField('slug', validators=[validators.DataRequired(), validators.Regexp('[\w-]+$', message="The slug must contain only letters, numbers, and dashes")])
  link = StringField('external link')
  body = TextAreaField('body', validators=[validators.DataRequired()])
  image = StringField('image')
  client = StringField('client (optional)')
  tags = StringField('list of languages, libraries, etc used in this project')
  featured = BooleanField('Feature this on the home page')

class ContactForm(Form):
  name = StringField('name', validators=[validators.DataRequired()])
  email = StringField('email', validators=[validators.DataRequired(), validators.Email()])
  message = TextAreaField('message', validators=[validators.DataRequired()])