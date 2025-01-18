from flask_login import UserMixin

from app import db

class Person(db.Model):
    __tablename__ = 'people'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    job = db.Column(db.Text)


    def __repr__(self):
        return f'Name: {self.name}, Age: {self.age}'
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    joindate = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User: {self.username}, Age: {self.role} is here since {self.joindate}>'

    def get_id(self):
        return self.uid
