from app.models import *

from app import chainadmin, db
from flask_admin.contrib.sqla import ModelView

'''
chainadmin interface
under the admin route
'''

chainadmin.add_view(ModelView(User, db.session))
chainadmin.add_view(ModelView(Stores, db.session))

class ChainAdminProductModelView(ModelView):
    column_formatters = {
        "store": lambda v, c, m, p: m.store.store_name
    }

chainadmin.add_view(ChainAdminProductModelView(Product, db.session))
chainadmin.add_view(ModelView(UseCategory, db.session))

chainadmin.add_view(ModelView(Charity, db.session))
chainadmin.add_view(ModelView(Chain, db.session))
chainadmin.add_view(ModelView(ProductCategory, db.session))
chainadmin.add_view(ModelView(Cart, db.session))
chainadmin.add_view(ModelView(ConnectCartProduct, db.session))
chainadmin.add_view(ModelView(HandlingCategory, db.session))
