import os
from typing import Any

from cachelib import FileSystemCache
from flask import Flask
from flask_session import Session

from intranet import flask
from intranet.alembic import migrate_db
from intranet.flask.authorization import authorization
from intranet.flask.dependable import Container
from intranet.flask.documents import documents
from intranet.flask.news import news
from intranet.flask.user_details import user_details
from intranet.flask.user_links import user_links


def no_cache_after_request(response: Any) -> Any:
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def setup() -> Flask:
    try:
        sessions = os.listdir(".flask_session")
        for session in sessions:
            os.remove(f".flask_session/{session}")
    except FileNotFoundError:
        pass

    app = Flask(
        __name__,
        static_folder="../front/static",
        template_folder="../front/templates",
    )

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
    app.register_blueprint(user_details)
    app.register_blueprint(user_links)
    app.register_blueprint(news)
    app.register_blueprint(documents)

    container.wire(
        modules=[
            flask.authorization,
            flask.user_details,
            flask.user_links,
            flask.news,
            flask.documents,
        ]
    )

    app.after_request(no_cache_after_request)

    if os.getenv("DB_MIGRATE", "") == "true":
        migrate_db()

    return app
