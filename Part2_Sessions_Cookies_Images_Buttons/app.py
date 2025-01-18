import pandas as pd
from flask import Flask, request, make_response, render_template, redirect, url_for, Response, send_from_directory, \
    jsonify, session, flash
import os
import uuid
import pandas

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")
app.secret_key = 'SOME KEY'
@app.route('/index')
def index():
    return render_template("index.html", message='')

@app.route('/set_data')
def set_data():
    session['name'] = 'Julian'
    session['other'] = 'Hello World'
    return render_template('index.html', message= 'Session Data has been set')

@app.route('/get_data')
def get_data():
    if (session):
        name = session.get('name')
        other = session.get('other')
        return render_template('index.html', message = f'Session Data: {name}, {other}')
    return render_template('index.html', message = "Missing Session Data")

@app.route('/clear_session')
def clear_session():
    session.clear()
    return render_template('index.html', message = 'Session data has been cleared')

@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('index.html', message = 'Cookie has been set'))
    response.set_cookie('cookie_name', 'cookie_value')
    return response

@app.route('/get_cookie')
def get_cookie():
    cookie_value = request.cookies.get('cookie_name')
    return render_template('index.html', message = f'Cookie Value: {cookie_value}')

@app.route('/remove_cookie')
def remove_cookie():
    response = make_response(render_template('index.html', message = 'Cookie has been removed'))
    response.set_cookie('cookie_name', expires=0)
    return response

@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '12345':
            flash('Login Successful')
            return render_template('index.html',message = 'Login Successful')
        else:
            flash('Login Failed')
            return render_template('index.html',message = 'Login Failed')
@app.route('/funwithimages')
def funwithimages():
    return render_template("funwithimages.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
