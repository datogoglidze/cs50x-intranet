from flask import Blueprint, render_template

from intranet.error import login_required

home = Blueprint("index", __name__, template_folder="../front/templates")


@home.get("/")
@login_required
def index_page() -> str:
    return render_template("index.html")
