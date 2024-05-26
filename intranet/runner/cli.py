import flask_session
from flask import Flask
from typer import Typer

from intranet import flask
from intranet.flask.authorization import authorization
from intranet.flask.index import home
from intranet.runner.factory import Container

cli = Typer(no_args_is_help=True, add_completion=False)


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


@cli.command()
def run(host: str = "0.0.0.0", port: int = 5000) -> None:
    setup().run(host=host, port=port)
