# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from whose_turn_is_it_anyway.settings import ProdConfig
from whose_turn_is_it_anyway.assets import assets
from whose_turn_is_it_anyway.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
    admin,
)
from whose_turn_is_it_anyway import public, user, activity
from flask_admin.contrib.sqla import ModelView
from whose_turn_is_it_anyway.user.models import User
from whose_turn_is_it_anyway.activity.models import Activity
from whose_turn_is_it_anyway.activity.filters import date_time_format, date_time_to_local

def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_filters(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    #cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    #admin.init_app(app)
    #admin.add_view(ModelView(User, db.session))
    #admin.add_view(ModelView(Activity, db.session))
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(activity.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_filters(app):
    app.jinja_env.filters['date_time_format'] = date_time_format
    app.jinja_env.filters['date_time_to_local'] = date_time_to_local

