from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap

from flask_admin import Admin


app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
logging.basicConfig(level=logging.DEBUG)
app.config.from_object(Config)
logging.info(f"Database url: {Config.SQLALCHEMY_DATABASE_URI}")

chainadmin = Admin(app, name='Feed', template_mode='bootstrap3')
from app.chain_admin_views import *

storeadmin = Admin(app, name='Feed', template_mode='bootstrap3', url='/sa', endpoint='/sa')
from app.store_admin_views import *

charityworker = Admin(app, name='Feed', template_mode='bootstrap3', url='/cw', endpoint='/cw')
from app.charity_worker_views import *

storekeeper = Admin(app, name='Feed', template_mode='bootstrap3', url='/sk', endpoint='/sk')
from app.storekeeper_views import *

from app import routes
from app.models import *




