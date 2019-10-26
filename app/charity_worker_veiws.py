from app.models import *

from app import charityworker, db
from flask_admin.contrib.sqla import ModelView

'''
veiws
'''

class CharityModelView(ModelView):
    form_args = dict(
        reuse_categories=dict(get_label=lambda x: x.name),
        handling_categories=dict(get_label=lambda x: x.name),
        product_categories=dict(get_label=lambda x: x.name),
    )



'''
charity worker interface
'''


# charityworker.add_view(ModelView(User, db.session))
charityworker.add_view(ModelView(Stores, db.session, endpoint='cw-stores'))
# charityworker.add_view(ModelView(Product, db.session))
# charityworker.add_view(ModelView(UseCategory, db.session))
#
charityworker.add_view(CharityModelView(Charity, db.session, endpoint='cw-charity'))
# charityworker.add_view(ModelView(Chain, db.session))
# charityworker.add_view(ModelView(ProductCategory, db.session))
# charityworker.add_view(ModelView(Cart, db.session))
# charityworker.add_view(ModelView(ConnectCartProduct, db.session))
# charityworker.add_view(ModelView(HandlingCategory, db.session))




