from app.models import *

from app import storekeeper, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
'''
veiws
'''

class UploadProductView(BaseView):
    @expose('/')
    def index(self):
        return 'birb!'


'''
storekeeper interface
'''
storekeeper.add_view(UploadProductView(endpoint='test'))

# storekeeper.add_view(ModelView(Product, db.session))
# storekeeper.add_view(ModelView(UseCategory, db.session))
# storekeeper.add_view(ModelView(ProductCategory, db.session))
# storekeeper.add_view(ModelView(HandlingCategory, db.session))





