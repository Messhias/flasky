"""
Intializing application

Instance of flask framework
"""

# chapter 5 - DATABASES
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, make_response, render_template, redirect, session, url_for, flash

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

# get absolute path of project directory
basedir = os.path.abspath(os.path.dirname(__file__))

from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'My SECRET_KEY'
bootstrap = Bootstrap(app)
moment = Moment(app)

# define models
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    """(User description)"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
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


@app.route('/', methods=['POST', 'GET'])
def index():
    """ Home page """
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['know'] = False
        else:
            session['know'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form,
                           name=session.get('name'),
                           know=session.get('know'))


@app.route('/user/<name>')
def user(name):
    """ Greetings user page """
    return render_template('user.html', name=name)
