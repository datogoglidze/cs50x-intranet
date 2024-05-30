import flask_session
from cachelib import FileSystemCache
from flask import Flask

from intranet import flask
from intranet.flask.authorization import authorization
from intranet.flask.dependable import Container
from intranet.flask.index import home


def no_cache_after_request(response):  # type: ignore
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def setup() -> Flask:
    app = Flask(__name__)

    container = Container()
    app.container = container  # type: ignore

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "cachelib"
    app.config["SESSION_CACHELIB"] = FileSystemCache("flask_session")

    flask_session.Session(app)

    app.register_blueprint(authorization)
    app.register_blueprint(home)

    container.wire(
        modules=[
            flask.authorization,
            flask.index,
        ]
    )

    app.after_request(no_cache_after_request)

    return app
