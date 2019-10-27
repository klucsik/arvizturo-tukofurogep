from app.models import *

from app import charityworker, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from geopy.distance import geodesic

'''
veiws
'''

class CharityModelView(ModelView):
    form_args = dict(
        reuse_categories=dict(get_label=lambda x: x.name),
        handling_categories=dict(get_label=lambda x: x.name),
        product_categories=dict(get_label=lambda x: x.name),
    )


"""
charity worker interface
"""


def is_selected_store(model):
    if current_user.charity is None:
        return False  # NOTE: Should not happen. Ugly check.
    return model in current_user.charity.charity_stores


def get_charity_store_distance(model):
    if current_user.charity is None:
        return "NA"
    if current_user.charity.latitude is None or current_user.charity.longitude is None:
        return "NA"
    if model.latitude is None or model.longitude is None:
        return "NA"
    pos_ch = (current_user.charity.latitude, current_user.charity.longitude)
    pos_st = (model.latitude, model.longitude)
    dist_km = geodesic(pos_ch, pos_st).kilometers
    return "{:.2f} km".format(dist_km)


class CharityWorkerStoresModelView(ModelView):
    column_filters = ("chain",)
    column_list = ("subscribed", "distance", "store_id", "store_name", "chain")
    column_labels = dict(selected="Subscribed")
    column_formatters = {
        "subscribed": lambda v, c, m, p: is_selected_store(m),
        "distance": lambda v, c, m, p: get_charity_store_distance(m),
    }

#columns = ["Selected", "Distance", "Name", "Address", "Chain", "ProdCats"]




charityworker.add_view(CharityWorkerStoresModelView(Stores, db.session, endpoint='cw-stores'))

charityworker.add_view(CharityModelView(Charity, db.session, endpoint='cw-charity'))




