from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap

from flask_admin import Admin


from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
logging.basicConfig(level=logging.DEBUG)
app.config.from_object(Config)
logging.info(f"Database url: {Config.SQLALCHEMY_DATABASE_URI}")




from app import routes
from app.models import *
admin = Admin(app, name='Feed', template_mode='bootstrap3')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Stores, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(UseCategory, db.session))

admin.add_view(ModelView(Charity, db.session))
admin.add_view(ModelView(Chain, db.session))
admin.add_view(ModelView(ProductCategory, db.session))
admin.add_view(ModelView(Cart, db.session))
admin.add_view(ModelView(ConnectCartProduct, db.session))
admin.add_view(ModelView(HandlingCategory, db.session))
