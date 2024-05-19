from flask import Blueprint, render_template

from intranet.error import login_required

home = Blueprint("index", __name__, template_folder="../front/templates")


@home.route("/")
@login_required  # type: ignore
def index() -> str:
    return render_template("index.html")
