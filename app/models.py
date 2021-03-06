'''
Created on Apr 14, 2018

@author: rich
'''

from datetime import datetime
from app import db, migrate, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)    

class User(UserMixin, db.Model):
    # This class represents a database table.
    id = db.Column(db.Integer, primary_key=True)  # @UndefinedVariable
    username = db.Column(db.String(64), index=True, unique=True)  # @UndefinedVariable
    email = db.Column(db.String(120), index=True, unique=True)  # @UndefinedVariable
    password_hash = db.Column(db.String(128))  # @UndefinedVariable
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # @UndefinedVariable
    about_me = db.Column(db.String(140))  # @UndefinedVariable
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)  # @UndefinedVariable
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0 
            
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())            

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
    
