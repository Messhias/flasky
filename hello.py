"""
Intializing application

Instance of flask framework
"""
from flask import Flask, make_response, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'My SECRET_KEY'
bootstrap = Bootstrap(app)
moment = Moment(app)


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
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name, don\'t you?')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time = datetime.utcnow(), name = session.get('name'), form = form)


@app.route('/user/<name>')
def user(name):
    """ Greetings user page """
    return render_template('user.html', name=name)
