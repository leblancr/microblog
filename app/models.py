'''
Created on Apr 14, 2018

@author: rich
'''

from datetime import datetime
from app import db, migrate, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # @UndefinedVariable
    username = db.Column(db.String(64), index=True, unique=True)  # @UndefinedVariable
    email = db.Column(db.String(120), index=True, unique=True)  # @UndefinedVariable
    password_hash = db.Column(db.String(128))  # @UndefinedVariable
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # @UndefinedVariable

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # @UndefinedVariable
    body = db.Column(db.String(140))  # @UndefinedVariable
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # @UndefinedVariable
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # @UndefinedVariable

    def __repr__(self):
        return '<Post {}>'.format(self.body)