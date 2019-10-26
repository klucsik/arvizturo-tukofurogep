from app.models import *

from app import storeadmin, db
from flask_admin.contrib.sqla import ModelView

'''
storeadmin interface

Csak a sjaát store-jához való dolgokhoz kell hozzáférjen
'''

# storeadmin.add_view(ModelView(User, db.session, endpoint='/stradmin-user'))
# storeadmin.add_view(ModelView(Product, db.session))
# storeadmin.add_view(ModelView(UseCategory, db.session))
#
# storeadmin.add_view(ModelView(Charity, db.session))
# storeadmin.add_view(ModelView(ProductCategory, db.session))
# storeadmin.add_view(ModelView(ConnectCartProduct, db.session))
# storeadmin.add_view(ModelView(HandlingCategory, db.session))