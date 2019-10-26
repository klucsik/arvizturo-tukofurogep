from flask_admin.contrib.sqla import ModelView


class CharityModelView(ModelView):
    form_args = dict(
        reuse_categories=dict(get_label=lambda x: x.name),
        handling_categories=dict(get_label=lambda x: x.name),
        product_categories=dict(get_label=lambda x: x.name),
    )
