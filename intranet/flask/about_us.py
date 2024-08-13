from __future__ import annotations

from flask import (
    Blueprint,
    render_template,
)

from intranet.error import login_required

about = Blueprint("about", __name__, template_folder="../front/templates")


@about.get("/about")
@login_required
def read_about() -> str:
    return render_template("about.html")
