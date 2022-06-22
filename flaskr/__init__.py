import os

from flask import Flask
from . import slurm_blueprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev",)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(slurm_blueprint.slurm_bp)
    # routing error page 404


    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>Page not found</h1>", 404

    return app
