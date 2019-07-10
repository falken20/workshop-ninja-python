# Copyright 2019
#
# Workshop Ninja Python

import logging

from flask import current_app, Flask, redirect, url_for


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Configuramos el modelo de datos
    with app.app_context():
        model = get_model()
        model.init_app(app)

    # Regsitramos el Ninja CRUD
    from .crud import crud
    app.register_blueprint(crud, url_prefix='/ninjas')

    # Adding ruta por defecto
    @app.route("/")
    def index():
        return redirect(url_for('crud.list'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


def get_model():
    from . import model_datastore
    model = model_datastore
    return model
