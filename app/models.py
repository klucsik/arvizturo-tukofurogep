from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import logging
from flask_login import UserMixin
from app import login
from flask import flash
'''
Primary entities
'''

managed_stores = db.Table('stores_managed_by_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=0)  # 0 if charity user, 1 if storekeeper, 2 if admin
    charity_id = db.Column(db.Integer)  # connect to Charity table if charity user
    chain_id = db.Column(db.Integer)  # connect to chain table if storekeeper or admin
    managed_stores = db.relationship('Stores', secondary=managed_stores, lazy='subquery', backref=db.backref('users', lazy=True))
    cart_is_open = db.Column(db.Boolean, default= True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(100))  # chain specific store id
    store_name = db.Column(db.String(100))
    chain_id = db.Column(db.Integer, db.ForeignKey('chain.id'), nullable=False)


charity_reuse_categories = db.Table('charity_reuse_categories',
    db.Column('charity_id', db.Integer, db.ForeignKey('charity.id'), primary_key=True),
    db.Column('reuse_id', db.Integer, db.ForeignKey('use_category.id'), primary_key=True)
)


charity_handling_categories = db.Table('charity_handling_categories',
    db.Column('charity_id', db.Integer, db.ForeignKey('charity.id'), primary_key=True),
    db.Column('handling_id', db.Integer, db.ForeignKey('handling_category.id'), primary_key=True)
)

charity_product_categories = db.Table('charity_product_categories',
    db.Column('charity_id', db.Integer, db.ForeignKey('charity.id'), primary_key=True),
    db.Column('product_category_id', db.Integer, db.ForeignKey('product_category.id'), primary_key=True)
)


class Charity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    category_id = db.Column(db.Integer)
    reuse_categories = db.relationship('UseCategory', secondary=charity_reuse_categories, lazy='subquery')
    handling_categories = db.relationship('HandlingCategory', secondary=charity_handling_categories, lazy='subquery')
    product_categories = db.relationship('ProductCategory', secondary=charity_product_categories, lazy='subquery')
    organisation_name = db.Column(db.String(200), unique=True)
    address = db.Column(db.String(200))
    contact_name = db.Column(db.String(100))
    contact_phone_number = db.Column(db.String(20))
    contact_email = db.Column(db.String(120), index=True, unique=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(200))
    store = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    quantity_dimension = db.Column(db.String(100))


class ProductMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('chain.id'), nullable=False)
    chain_product_id = db.Column(db.String(200))
    name = db.Column(db.String(200))
    product_category = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    handling_category = db.Column(db.Integer, db.ForeignKey('handling_category.id'), nullable=False)
    reuse_category = db.Column(db.Integer, db.ForeignKey('use_category.id'), nullable=False)


'''
higher level entities
'''


class Chain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    stores = db.relationship(Stores, backref='chain', lazy=True)


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

    def makeorder(self, user_id):
        try:
            cart_items = Cart.query.filter_by(user_id=user_id).all()
            for item in cart_items:
                order_row= Order(user_id=item.user_id, product_id = item.product_id)
                db.session.add(order_row)
                db.session.flush()
                db.session.commit()
            ordering_user = User.query.filter_by(user_id=user_id).first()
            ordering_user.cart_is_open = False
        except Exception as e:
            logging.error('Hulladék keresés error: ' + str(e))
            flash(f' Something went wrong: ' + str(e) )

# def test_makeorder():
#     Cart.makeorder()





class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)


'''
connector tables
'''


class ConnectCartProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

'''
infotables 
'''


class UseCategory(db.Model):
    '''
    for example human consumable , animal consumable
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))

class HandlingCategory(db.Model):
    '''
    for example requeires freezing
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))


'''
misc
'''

@login.user_loader
def load_user(id):
    return User.query.get(int(id))