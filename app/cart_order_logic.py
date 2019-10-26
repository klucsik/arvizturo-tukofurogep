from app.models import *


def makeorder(user_id):
    try:
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        for item in cart_items:
            order_row = Order(user_id=item.user_id, product_id=item.product_id)
            db.session.add(order_row)
            db.session.flush()
            db.session.commit()
        ordering_user = User.query.filter_by(id=user_id).first()
        ordering_user.cart_is_open = False
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logging.error('makeorder went wrong: ' + str(e))
        flash(f' Something went wrong: ' + str(e))


def add_to_cart(user_id, product_id):
    try:
        ordering_user = User.query.filter_by(id=user_id).first()
        if ordering_user.cart_is_open:
             if Cart.query.filter_by(product_id=product_id).first():
                 raise Exception("Item already in someones cart")
             else:
                row_to_cart = Cart(user_id=user_id, product_id=product_id)
                db.session.add(row_to_cart)
                db.session.flush()
                db.session.commit()
        else:
            raise Exception("User's cart is not open")
        return row_to_cart
    except Exception as e:
        logging.error('makeorder went wrong: ' + str(e))
        flash(f' Something went wrong: ' + str(e))




