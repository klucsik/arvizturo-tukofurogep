from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=0)  # 0 if charity user, 1 if storekeeper, 2 if admin
    charity_id = db.Column(db.Integer)  # connect to Charity table if charity user
    store_list_id = db.Column(db.Integer)  # connect to store list table -- which stores is affected by this user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Charity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    category_id = db.Column(db.Integer)


class StoreList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer)  # query for this id, return a lsit of stores
    store_id = db.Column(db.String(64))
    store_name = db.Column(db.String(100))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class RequestType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
