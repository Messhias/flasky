"""
Intializing application

Instance of flask framework
"""

# chapter 5 - DATABASES
import os
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, make_response, render_template, redirect, session, url_for, flash
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from threading import Thread

# get absolute path of project directory
basedir = os.path.abspath(os.path.dirname(__file__))

from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[FLASKY]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <messhias@gmail.com>'
app.config['MAIL_SERVER'] = 'in-v3.mailjet.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'My SECRET_KEY'
bootstrap = Bootstrap(app)
moment = Moment(app)

migrate = Migrate(app, db)

mail = Mail(app)

# define models
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    middlename = db.Column(db.String(60))
    lastname = db.Column(db.String(60))
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    """(User description)"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    level = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    ''' new page not found  '''
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    ''' new page for internal server error '''
    return render_template('500.html'), 500


@app.route('/cookie')
def cookie():
    """
    Example of cookie usage
    @return render
    """
    response = make_response('<h1>This document carries a cookie!')
    response.set_cookie('answer', '42')
    return render_template('cookie.html', response=response)


@app.route('/404')
def _404():
    """ 404 PAGE """
    return '<h1>Not foound, returning a 404 error page</h1>', 404



@app.route('/user/<name>')
def user(name):
    """ Greetings user page """
    return render_template('user.html', name=name)


# Function to intialize the shell processor contexts
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


def send_ansyc_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_ansyc_email, args=[app, msg])
    thr.start()
    return thr
