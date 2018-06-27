"""
Intializing application

Instance of flask framework
"""
from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/cookie')
def cookie():
    """ Example of cookie usage """
    response = make_response('<h1>This document carries a cookie!')
    response.set_cookie('answer', '42')
    return response


@app.route('/404')
def _404():
    """ 404 PAGE """
    return '<h1>Not foound, returning a 404 error page</h1>', 404


@app.route('/')
def index():
    """ Home page """
    user_agent = request.headers.get('User-Agent')
    return '<h1>Hello World, your browser is {}</h1>'.format(user_agent)


@app.route('/user/<name>')
def user(name):
    """ Greetings user page """
    return '<h1>Hello, {}</h1>'.format(name)
