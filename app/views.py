from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, login_manager
from .forms import PageForm, ProjectForm, ContactForm, LoginForm
from .models import User, Project, Page
from config import POSTS_PER_PAGE, ADMIN_EMAIL

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
  return render_template("login.html", form=form, title='Login')

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    g.user.is_authenticated = False
    logout_user()
    return redirect(url_for('index'))

# un-comment to allow creation of new users
# @app.route('/create-new-user', methods=['GET', 'POST'])
def create_user():
  form = LoginForm()
  next_url = request.args.get('next') or url_for('index')

  if form.validate_on_submit():
    username = form.username.data
    user = User.query.get(username)

    if user is None:
      user = User(id=username, email=ADMIN_EMAIL)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      login_user(user, True)
      flash(u'New user %s created' % username)
      return redirect(url_for('index'))
    else:
      flash(u'The username %s already exists' % username)

  return render_template("login.html", form=form, title='Create New User')

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

# Portfolio
@app.route('/portfolio')
def portfolio(page=1):
  projects = Project.query.order_by(Project.timestamp.desc()) #.paginate(project, POSTS_PER_PAGE, True)
  return render_template('portfolio.html', title='Portfolio', projects=projects)

@app.route('/portfolio/<slug>')
def project(slug):
  project = Project.query.filter_by(slug=slug).first()
  if project is None:
    flash('The URL "/portfolio/%s" was not found' % slug)
    return redirect(url_for('portfolio'))
  return render_template('project.html', title=project.title, project=project)

@app.route('/portfolio/new', methods=['GET', 'POST'])
@login_required
def add_project():
  form = ProjectForm()

  if g.user is None or not g.user.is_authenticated:
    return redirect(url_for('login'))

  if form.validate_on_submit():
    flash('Project created: %s' % form.title.data)
    project = Project(
      title=form.title.data,
      slug=form.slug.data,
      image=form.image.data,
      link=form.link.data,
      client=form.client.data,
      tags=form.tags.data,
      body=form.body.data,
      featured=form.featured.data,
      timestamp=datetime.now())
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('project', slug=form.slug.data))

  return render_template('project_add_edit.html', form=form, action='Create', title='New Project')

@app.route('/portfolio/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(slug):
  project = Project.query.filter_by(slug=slug).first()
  form = ProjectForm(obj=project)

  if g.user is None or not g.user.is_authenticated:
    return redirect(url_for('login'))

  if form.validate_on_submit():
    flash('Project updated')
    project.title=form.title.data
    project.slug=form.slug.data
    project.image=form.image.data
    project.link=form.link.data
    project.client=form.client.data
    project.tags=form.tags.data
    project.body=form.body.data
    project.featured=form.featured.data
    project.timestamp=datetime.now()
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('project', slug=form.slug.data))

  return render_template('project_add_edit.html', form=form, action='Edit', title='Edit Project')



