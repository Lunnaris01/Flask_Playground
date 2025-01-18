import re

from flask import render_template, request, url_for, redirect, flash, session
from flask_login import login_user,logout_user,login_required,current_user

from models import Person, User

def registrer_routes(app, db, bcrypt):

    @app.route('/')
    def index():

        if current_user.is_authenticated:
            return render_template('index.html',message='Welcome Back')
        else:
            return render_template('index.html',message='Hello New User')


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form['username']
            username = username.strip()
            if not re.match(u'^[A-Za-z][A-Za-z0-9_]*$', username):
                flash('Username must contain only letters, numbers and underscores','error')
                return redirect(url_for('signup'))
            if username in [user.username for user in User.query.all()]:
                flash('Username already taken','error')
                return redirect(url_for('signup'))
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password)
            user = User(username=username, password=hashed_password,role='user')

            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered','success')
            return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form['username']
            username = username.strip()
            if not re.match(u'^[A-Za-z][A-Za-z0-9_]*$', username):
                flash('Invalid Username!', 'error')
                return redirect(url_for('login'))
            password = request.form['password']
            user = User.query.filter(User.username == username).first()
            if bcrypt.check_password_hash(user.password,password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Wrong Password or Username!', 'error')
                return redirect(url_for('login'))

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('index'))


    @app.route('/simple',methods=['GET','POST'])
    def simple():
        if request.method == 'GET':
            people = Person.query.all()

            return render_template('simple.html',message='This is the Landing Text',people=Person.query.all(), maxNameLen=getMaxNameLen())
        elif request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            job = request.form['job']
            person = Person(name=name,age=age,job=job)
            db.session.add(person)
            db.session.commit()
            return render_template('simple.html',message='Entered new Entry!',people=Person.query.all(), maxNameLen=getMaxNameLen())
    @app.route('/simple_delete/<pid>',methods=['DELETE'])
    def simple_delete(pid):
        Person.query.filter(Person.pid == pid).delete()
        db.session.commit()
        return render_template('simple.html', message='Removed an Entry!', people=Person.query.all(), maxNameLen=getMaxNameLen())

    def getMaxNameLen():
        people = Person.query.all()
        if len(people) == 0:
            return 0
        return max(len(person.name) for person in people)