from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash

# Create User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    password = db.Column(db.String(128), nullable=False)
    # List of Posts - One to Many
    posts = db.relationship('Post', backref='author', lazy=True)

    # @property
    # def password(self):
    #     raise AttributeError("Password is not readable")

    # @password.setter
    # def password(self, password):
    #     self.password = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"Name: {self.name} - Email: {self.email}"
    
# Create Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # Create a Foreign Key - Many to One
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))