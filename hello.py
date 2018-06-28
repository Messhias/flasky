"""
Intializing application

Instance of flask framework
"""
from flask import Flask, request, make_response, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


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


@app.route('/')
def index():
    """ Home page """
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', response=user_agent)


@app.route('/user/<name>')
def user(name):
    """ Greetings user page """
    return render_template('user.html', name=name)
