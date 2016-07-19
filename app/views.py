from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, login_manager
from .forms import PageForm, ProjectForm, ContactForm, LoginForm
from .models import User, Project, Page
from config import POSTS_PER_PAGE

@app.before_request
def before_request():
  g.user = current_user

@login_manager.user_loader
def load_user(id):
  return User.query.get(id)

@app.route('/')
@app.route('/index')
@app.route('/page/<int:page>')
def index(page=1):
  return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
  
  if g.user is not None and g.user.is_authenticated:
    return redirect(url_for('index'))

  form = LoginForm()
  next_url = request.args.get('next') or url_for('index')

  if form.validate_on_submit():
    user = User.query.get(form.username.data)
    if user:
      if User.check_password(user, form.password.data):
        login_user(user, True)
        return redirect(next_url)
      else:
        flash(u'Access Denied: incorrect password')
    else:
      flash(u'Access Denied. The user %s does not exist.' % form.username.data)

  # Show the login form for GET requests
  return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    g.user.is_authenticated = False
    logout_user()
    return redirect(url_for('index'))

#Need to update this
@app.route('/create-new-user')
def create_user(resp):
  next_url = request.args.get('next') or url_for('index')
  if resp is None:
    flash(u'You denied the request to sign in.')
    return redirect(next_url)

  user = User.query.filter_by(social_id=fb_user.data['id']).first()
  if user is None:
    user = User(social_id=fb_user.data['id'], nickname=fb_user.data['name'], email=fb_user.data['email'])
    db.session.add(user)
    db.session.commit()
    flash(u'New user created: %s' % fb_user.data['name'])
    return redirect(url_for('index'))

  login_user(user, True)
  flash('You were signed in as %s' % fb_user.data['name'])
  return redirect(next_url)

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if form.validate_on_submit():
    flash('Thank you for your message. We\'ll get in touch as soon as we can, but please be patient -- we may not have access to the internet for a while.')
    return redirect(url_for('contact'));

  return render_template('contact.html', title='Contact Us', form=form)

# Generic Pages
@app.route('/<slug>')
def page(slug):
  page = Page.query.filter_by(slug=slug).first()
  if page is None:
    flash('The URL "%s" was not found' % slug)
    return redirect(url_for('index'))
  return render_template('page.html', title=page.title, page=page)

@app.route('/page/new', methods=['GET', 'POST'])
@login_required
def add_page():
  form = PageForm()

  if form.validate_on_submit():
    flash('Page created: %s' % form.title.data)
    page = Page(title=form.title.data, slug=form.slug.data, body=form.body.data)
    db.session.add(page)
    db.session.commit()
    return redirect(url_for('page', slug=form.slug.data))

  return render_template('page_add_edit.html', form=form, action='Create', title='New Page')

@app.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_page(slug):
  page = Page.query.filter_by(slug=slug).first()
  form = PageForm(obj=page)

  if form.validate_on_submit():
    flash('Page updated')
    page.title = form.title.data
    page.slug = form.slug.data
    page.body = form.body.data
    db.session.commit()
    return redirect(url_for('page', slug=form.slug.data))

  return render_template('page_add_edit.html', form=form, action='Edit', title='Edit Page')

@app.route('/<slug>/delete')
@login_required
def delete_page(slug):
  page = Page.query.filter_by(slug=slug).first()
  title = page.title
  if page is None:
    flash('Page not found.')
    return redirect(url_for('index'))

  db.session.delete(page)
  db.session.commit()
  flash('"%s" has been deleted' % title)
  return redirect(url_for('index'))



