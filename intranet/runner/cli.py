import flask_session
from flask import Flask
from typer import Typer

from intranet.flask.authorization import authorization
from intranet.flask.index import home

cli = Typer(no_args_is_help=True, add_completion=False)

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = ".flask_session"
flask_session.Session(app)

app.register_blueprint(authorization)
app.register_blueprint(home)


@app.after_request
def after_request(response):  # type: ignore
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@cli.command()
def run(host: str = "0.0.0.0", port: int = 5000) -> None:
    app.run(host=host, port=port)
