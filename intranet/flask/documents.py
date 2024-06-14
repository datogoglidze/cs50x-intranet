import datetime
import os
from io import BytesIO
from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from werkzeug import Response

from intranet.core.user_details import UserDetailsRepository
from intranet.core.user_documents import UserDocument
from intranet.error import apology, login_required
from intranet.flask.dependable import Container

documents = Blueprint("documents", __name__, template_folder="../front/templates")


@documents.get("/documents")
@inject
@login_required
def user_details_page(
    details: UserDetailsRepository = Provide[Container.user_details_repository],
) -> str:
    if not os.path.exists("documents"):
        os.makedirs("documents")
    _documents = os.listdir("documents")
    last_name = details.read(session["user_id"]).last_name
    user_documents = [file for file in _documents if last_name in file]

    return render_template("user_documents.html", documents=user_documents)


@documents.get("/documents/<filename>")
@login_required
def pdf_viewer(filename: str) -> Response:
    return send_from_directory("../../documents", filename)


@documents.post("/documents")
@inject
@login_required
def create_document(
    details: UserDetailsRepository = Provide[Container.user_details_repository],
) -> Response | tuple[str, int]:
    user = details.read(session["user_id"])
    document = UserDocument(
        id=str(uuid4()),
        first_name=user.first_name,
        last_name=user.last_name,
        dates=request.form.get("dates", ""),
        category=request.form.get("category", ""),
    )

    if not document.first_name or not document.last_name:
        return apology("must fill details", 403)

    if not document.dates:
        return apology("must specify date", 403)

    generate_document_with(
        document.id,
        document.first_name,
        document.last_name,
        document.dates,
        document.category,
    )

    return redirect("/documents")


def generate_document_with(
    document_id: str,
    first_name: str,
    last_name: str,
    dates: str,
    category: str,
) -> None:
    pdfmetrics.registerFont(
        TTFont(
            "GeorgianFontNormal",
            "intranet/assets/fonts/DejaVuSans.ttf",
        )
    )
    pdfmetrics.registerFont(
        TTFont(
            "GeorgianFontBold",
            "intranet/assets/fonts/DejaVuSans-Bold.ttf",
        )
    )
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("GeorgianFontNormal", 12)

    # Create a PDF document
    p.drawString(100, 750, "Book Catalog")

    y = 700

    # TODO: Generalize pdf drawing (maybe with for loop while reading file)
    p.drawString(100, y, f"ID: {document_id}")
    p.drawString(100, y - 20, f"Author: {first_name}")
    p.drawString(100, y - 40, f"Year: {dates}")
    y -= 60

    p.showPage()
    p.save()

    buffer.seek(0)

    new_document = (
        f"documents/"
        f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        f"-{last_name}"
        f"-{first_name}"
        f"-{category}"
        f".pdf"
    )

    with open(new_document, "wb") as f:
        f.write(buffer.getvalue())

    buffer.close()
