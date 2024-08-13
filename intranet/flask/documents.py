from __future__ import annotations

import datetime
import os
from dataclasses import dataclass, field
from enum import Enum
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
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from werkzeug import Response

from intranet.core.documents import Document
from intranet.core.user_details import UserDetailsRepository
from intranet.error import apology, login_required
from intranet.flask.dependable import Container

documents = Blueprint("documents", __name__, template_folder="../front/templates")


@documents.get("/documents")
@inject
@login_required
def user_details_page() -> str:
    if not os.path.exists("documents"):
        os.makedirs("documents")
    _documents = os.listdir("documents")
    user_documents = [file for file in _documents if session["user_id"] in file]

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
    document = Document(
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
        DocumentGenerator(document.dates).with_category(
            DocumentCategory(document.category)
        ),
        document.first_name,
        document.last_name,
        document.category,
    ).with_layout(
        page_width=8.5 * inch,
        page_height=11 * inch,
        margin=50,
        line_height=18,
    )

    return redirect("/documents")


@dataclass
class GenerateDocument:
    body: str
    first_name: str
    last_name: str
    category: str

    id: str = field(default_factory=lambda: str(uuid4()))

    def with_header(self) -> str:
        with open(
            "document_templates/head.txt",
            "r",
            encoding="utf-8",
        ) as file:
            header = file.read()

        updated_header = header.replace("!<<DOC_ID>>", self.id)
        updated_header = updated_header.replace("!<<FIRST_NAME>>", self.first_name)
        updated_header = updated_header.replace("!<<LAST_NAME>>", self.last_name)

        return updated_header

    def with_footer(self) -> str:
        with open(
            "document_templates/foot.txt",
            "r",
            encoding="utf-8",
        ) as file:
            footer = file.read()

        return footer

    def with_layout(
        self,
        page_width: float,
        page_height: float,
        margin: int,
        line_height: int,
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

        updated_text = self.with_header() + self.body + self.with_footer()

        with BytesIO() as buffer:
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("GeorgianFontNormal", 12)

            # Start from a reasonable position on the first page
            y = page_height - margin

            for line in updated_text.split("\n"):
                y = PdfConstructor(
                    page_width,
                    page_height,
                    margin,
                    line_height,
                ).draw_wrapped_text(line, pdf, y)
                if y < margin:
                    pdf.showPage()
                    pdf.setFont("GeorgianFontNormal", 12)
                    y = page_height - margin

            pdf.showPage()
            pdf.save()

            buffer.seek(0)

            with open(self.with_name(), "wb") as f:
                f.write(buffer.getvalue())

    def with_name(self) -> str:
        return (
            f"documents/"
            f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
            f"-{self.last_name}"
            f"-{self.first_name}"
            f"-{self.category}"
            f"-{session['user_id']}"
            f".pdf"
        )


class DocumentCategory(Enum):
    paid_vacation: str = "paid_vacation"
    unpaid_vacation: str = "unpaid_vacation"


@dataclass
class DocumentGenerator:
    dates: str

    def with_category(self, category: DocumentCategory) -> str:
        return self.from_template(category)

    def from_template(self, category: DocumentCategory) -> str:
        with open(
            f"document_templates/{category.value}_body.txt",
            "r",
            encoding="utf-8",
        ) as file:
            template_text = file.read()

        updated_text = template_text.replace("!<<DATE>>", self.dates)

        return updated_text


@dataclass
class PdfConstructor:
    page_width: float
    page_height: float
    margin: int
    line_height: int

    def draw_wrapped_text(self, line: str, pdf: Canvas, y_location: float) -> float:
        words = line.split()
        write_line = ""

        for word in words:
            test_line = f"{write_line} {word}".strip()
            if (
                pdf.stringWidth(test_line, "GeorgianFontNormal", 12)
                <= self.page_width - 2 * self.margin
            ):
                write_line = test_line
            else:
                pdf.drawString(self.margin, y_location, write_line)
                y_location -= self.line_height
                write_line = word
                if y_location < self.margin:
                    pdf.showPage()
                    pdf.setFont("GeorgianFontNormal", 12)
                    y_location = self.page_height - self.margin
        pdf.drawString(self.margin, y_location, write_line)

        return y_location - self.line_height
