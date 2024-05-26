from flask import Blueprint, render_template

from intranet.error import login_required

home = Blueprint("index", __name__, template_folder="../front/templates")


@home.after_request
def after_request(response):  # type: ignore
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@home.route("/")
@login_required  # type: ignore
def index() -> str:
    return render_template("index.html")
