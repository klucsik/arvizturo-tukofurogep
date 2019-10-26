from app.models import *
import logging
from flask import flash

def add_to_cart(user_id, product_id):
    try:
        ordering_user = User.query.filter_by(id=user_id).first()
        product = Product.query.filter_by(id=product_id)
        if ordering_user.cart_is_open:
             if product.state == 'listed':
                 raise Exception("Item already in someones cart")
             else:
                row_to_cart = Cart(user_id=user_id, product_id=product_id)
                db.session.add(row_to_cart)

                product.state = 'in_cart'
                db.session.flush()
                db.session.commit()
        else:
            raise Exception("User's cart is not open")
        return row_to_cart
    except Exception as e:
        logging.error('add to cart went wrong: ' + str(e))
        flash(' Something went wrong: ' + str(e))


def makeorder(user_id):
    try:
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        for cart_item in cart_items:
            product = Product.query.filter_by(id=cart_item.product_id)
            order_row = Order(user_id=cart_item.user_id, product_id=cart_item.product_id)
            db.session.add(order_row)
            cart_item.delete()
            product.state = 'ordered'
            db.session.flush()
            db.session.commit()
        ordering_user = User.query.filter_by(id=user_id).first()
        ordering_user.cart_is_open = False
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logging.error('makeorder went wrong: ' + str(e))
        flash(' Something went wrong: ' + str(e))


def fulfill_order(user_id):
    try:
        order_items = Order.query.filter_by(user_id=user_id).all()
        for order_item in order_items:
            product = Product.query.filter_by(id=order_item.product_id)
            fulfilled_row = Fulfilled(user_id=order_item.user_id, product_id=order_item.product_id)
            db.session.add(fulfilled_row)
            order_item.delete()
            product.state = 'fulfilled'
            db.session.flush()
            db.session.commit()
        ordering_user = User.query.filter_by(id=user_id).first()
        ordering_user.cart_is_open = True
        db.session.flush()
        db.session.commit()

    except Exception as e:
        logging.error('fulfill went wrong: ' + str(e))
        flash(' Something went wrong: ' + str(e))




