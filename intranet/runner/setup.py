from typing import Any

from cachelib import FileSystemCache
from flask import Flask
from flask_session import Session

from intranet import flask
from intranet.flask.authorization import authorization
from intranet.flask.dependable import Container
from intranet.flask.index import home
from intranet.flask.user_details import user_details


def no_cache_after_request(response: Any) -> Any:
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
    app.config["SESSION_CACHELIB"] = FileSystemCache(
        cache_dir=".flask_session",
        threshold=500,
    )

    Session(app)

    app.register_blueprint(authorization)
    app.register_blueprint(home)
    app.register_blueprint(user_details)

    container.wire(
        modules=[
            flask.authorization,
            flask.index,
            flask.user_details,
        ]
    )

    app.after_request(no_cache_after_request)

    return app
