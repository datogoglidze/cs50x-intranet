import datetime
from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from docx import Document
from docx2pdf import convert
from flask import Blueprint, redirect, render_template, request, session
from werkzeug import Response

from intranet.core.user_details import UserDetailsRepository
from intranet.core.user_documents import UserDocument
from intranet.error import apology, login_required
from intranet.flask.dependable import Container

user_documents = Blueprint(
    "user_documents", __name__, template_folder="../front/templates"
)


@user_documents.get("/documents")
@login_required
def user_details_page() -> str:
    return render_template("user_documents.html")


@user_documents.post("/documents")
@inject
@login_required
def create_document(
    details: UserDetailsRepository = Provide[Container.user_details_repository],
) -> Response | tuple[str, int]:
    user_details = details.read(session["user_id"])
    user_document = UserDocument(
        id=str(uuid4()),
        first_name=user_details.first_name,
        last_name=user_details.last_name[:-1] + "ის",
        dates=request.form.get("dates", ""),
    )

    if not user_document.first_name or not user_document.last_name:
        return apology("must fill details", 403)

    if not user_document.dates:
        return apology("must specify date", 403)

    generate_document(
        user_document.id,
        user_document.first_name,
        user_document.last_name,
        user_document.dates,
    )

    return redirect("/user-details")


def generate_document(_id: str, first_name: str, last_name: str, dates: str) -> None:
    document = Document("document_templates/vacation_template.docx")
    document.styles["Normal"].font.name = "Sylfaen"

    for paragraph in document.paragraphs:
        paragraph.text = paragraph.text.replace(
            "!<<DOC_ID>>",
            _id,
        )
        paragraph.text = paragraph.text.replace(
            "!<<FIRST_NAME>>",
            first_name,
        )
        paragraph.text = paragraph.text.replace(
            "!<<LAST_NAME>>",
            last_name,
        )
        paragraph.text = paragraph.text.replace(
            "!<<DATE>>",
            dates,
        )

    document_name = f"{datetime.datetime.now().date()} {last_name} {_id}"
    document.save("vacations/" + document_name + ".docx")
    convert(
        f"vacations/{document_name}.docx",
        f"vacations/{document_name}.pdf",
    )
