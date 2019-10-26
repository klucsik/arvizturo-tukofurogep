from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

'''
Primary entities
'''


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=0)  # 0 if charity user, 1 if storekeeper, 2 if admin
    charity_id = db.Column(db.Integer)  # connect to Charity table if charity user
    chain_id = db.Column(db.Integer)  # connect to chain table if storekeeper or admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(100))
    store_name = db.Column(db.String(100))


class Charity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    category_id = db.Column(db.Integer)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(200))
    name = db.Column(db.String(200))
    store = db.Column(db.Integer)
    FoodCategory = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    quantity_dimension = db.Column(db.String(100))



'''
higher level entities
'''


class Chain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)



'''
connector tables
'''


class UserStores(db.Model):  # todo: define foreign keys
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # which stores is affected by this user
    store_id = db.Column(db.String(100))


class BasketProduct(db.Model):
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


class FoodCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class RequestType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

