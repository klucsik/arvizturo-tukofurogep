# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     external_id = db.Column(db.String(200))
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
#     store = orm.relationship("Stores")
#     name = db.Column(db.String(200))
#     quantity = db.Column(db.Integer)
#     quantity_dimension = db.Column(db.String(100))
#     state = db.Column(db.String(100), default='listed')
#     # listed = available,
#     # in_cart = in someones cart/in cart table,
#     # ordered = in order table
#     # fullfilled = delivered to charities, end state
#     product_category = db.Column(db.Integer, db.ForeignKey('product_category.id'))
#     handling_category = db.Column(db.Integer, db.ForeignKey('handling_category.id'))
#     use_category = db.Column(db.Integer, db.ForeignKey('use_category.id'))
#
#
# class ProductMapping(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     chain_id = db.Column(db.Integer, db.ForeignKey('chain.id'), nullable=False)
#     chain_product_id = db.Column(db.String(200))
#     name = db.Column(db.String(200))
#     product_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
#     product_category = orm.relationship("ProductCategory")
#     handling_category_id = db.Column(db.Integer, db.ForeignKey('handling_category.id'), nullable=False)
#     handling_category = orm.relationship("HandlingCategory")
#     reuse_category_id = db.Column(db.Integer, db.ForeignKey('use_category.id'), nullable=False)
#     reuse_category = orm.relationship("UseCategory")

from app.models import *


def product_create():
    # todo
    external_id = 1
    store_id = 1
    quantity = 1
    quantity_dimension = 1
    product_category = 1
    handling_category = 1
    use_category = 1
    name = 1

    row = Product(external_id=external_id,
                  quantity=quantity,
                  store_id=store_id,
                  quantity_dimension=quantity_dimension,
                  product_category=product_category,
                  handling_category=handling_category,
                  use_category=use_category,
                  name=name
                  )
    db.session.add(row)
    db.session.flush()
    db.session.commit()
    return row

