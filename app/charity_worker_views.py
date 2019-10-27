from app.models import *

from app import charityworker, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from geopy.distance import geodesic
from flask_admin.babel import lazy_gettext, gettext, ngettext
from flask_admin.actions import action
from flask import flash
from flask_admin.contrib.sqla import tools

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
    column_list = ("subscribed", "distance", "address", "store_name", "chain", "store_id")
    column_labels = dict(selected="Subscribed")
    can_delete = False
    can_edit = False
    column_formatters = {
        "subscribed": lambda v, c, m, p: is_selected_store(m),
        "distance": lambda v, c, m, p: get_charity_store_distance(m),
    }

    @action('subscribe',
            lazy_gettext('Subscribe'))
    def action_subscribe(self, ids):
        try:
            query = tools.get_query_for_ids(self.get_query(), self.model, ids)
            count = 0
            stores = current_user.charity.charity_stores
            for m in query.all():
                if m not in stores:
                    stores.append(m)
                    count += 1

            self.session.commit()

            flash(ngettext('Successfully subscribed to store.',
                           'Subscribed to %(count)s stores.',
                           count,
                           count=count), 'success')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed to subscribe to stores. %(error)s', error=str(ex)), 'error')

    @action('unsubscribe',
            lazy_gettext('Unsubscribe'))
    def action_unsubscribe(self, ids):
        try:
            query = tools.get_query_for_ids(self.get_query(), self.model, ids)
            count = 0
            stores = current_user.charity.charity_stores
            for m in query.all():
                if m in stores:
                    stores.remove(m)
                    count += 1

            self.session.commit()

            flash(ngettext('Successfully unsubscribed from stores.',
                           'Unsubscribed from %(count)s stores.',
                           count,
                           count=count), 'success')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed to unsubscribe from stores. %(error)s', error=str(ex)), 'error')


charityworker.add_view(CharityWorkerStoresModelView(Stores, db.session, endpoint='cw-stores'))

charityworker.add_view(CharityModelView(Charity, db.session, endpoint='cw-charity'))




