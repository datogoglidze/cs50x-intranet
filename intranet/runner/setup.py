import flask_session
from flask import Flask

from intranet import flask
from intranet.flask.authorization import authorization
from intranet.flask.dependable import Container
from intranet.flask.index import home


def setup() -> Flask:
    container = Container()
    app = Flask(__name__)
    app.container = container  # type: ignore

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_FILE_DIR"] = ".flask_session"

    flask_session.Session(app)

    app.register_blueprint(authorization)
    app.register_blueprint(home)

    container.wire(
        modules=[
            flask.authorization,
            flask.index,
        ]
    )

    return app
