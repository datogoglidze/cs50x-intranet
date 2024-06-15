import datetime
import os
from dataclasses import dataclass, field
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
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
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

    GenerateDocument(
        document.first_name,
        document.last_name,
        document.dates,
        document.category,
    ).generate_document_with()

    return redirect("/documents")


@dataclass
class GenerateDocument:
    first_name: str
    last_name: str
    dates: str
    category: str

    id: str = field(default_factory=lambda: str(uuid4()))

    def generate_document_with(self):
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

        updated_text = self.replace_fields()

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("GeorgianFontNormal", 12)

        page_width, page_height = letter
        margin = 50
        y = page_height - margin  # Start from a reasonable position on the first page
        line_height = 18  # Line height for normal text

        def draw_wrapped_text(
            text: str,
            pdf: Canvas,
            _margin: int,
            y_location: float,
            _max_width: float,
            _line_height: int,
        ) -> float:
            words = text.split()
            _line = ""
            for word in words:
                test_line = f"{_line} {word}".strip()
                if pdf.stringWidth(test_line, "GeorgianFontNormal", 12) <= _max_width:
                    _line = test_line
                else:
                    pdf.drawString(_margin, y_location, _line)
                    y_location -= _line_height
                    _line = word
                    if y_location < margin:
                        pdf.showPage()
                        pdf.setFont("GeorgianFontNormal", 12)
                        y_location = page_height - margin
            pdf.drawString(_margin, y_location, _line)
            return y_location - _line_height

        max_width = page_width - 2 * margin

        for line in updated_text.split("\n"):
            y = draw_wrapped_text(line, p, margin, y, max_width, line_height)
            if y < margin:
                p.showPage()
                p.setFont("GeorgianFontNormal", 12)
                y = page_height - margin

        p.showPage()
        p.save()

        buffer.seek(0)

        with open(self.with_name(), "wb") as f:
            f.write(buffer.getvalue())

        buffer.close()

    def with_name(self):
        return (
            f"documents/"
            f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
            f"-{self.last_name}"
            f"-{self.first_name}"
            f"-{self.category}"
            f".pdf"
        )

    def with_template(self):
        with open(
            "document_templates/vacation_template.txt",
            "r",
            encoding="utf-8",
        ) as file:
            template_text = file.read()

        return template_text

    def replace_fields(self) -> str:
        template_text = self.with_template()

        updated_text = template_text.replace("!<<DOC_ID>>", self.id)
        updated_text = updated_text.replace("!<<FIRST_NAME>>", self.first_name)
        updated_text = updated_text.replace("!<<LAST_NAME>>", self.last_name)
        updated_text = updated_text.replace("!<<DATE>>", self.dates)

        return updated_text
