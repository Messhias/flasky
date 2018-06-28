"""
Intializing application

Instance of flask framework
"""
from flask import Flask, request, make_response, render_template

app = Flask(__name__)


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
