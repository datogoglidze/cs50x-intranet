from __future__ import annotations

import os
from dataclasses import dataclass
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
    url_for,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from werkzeug import Response

from intranet.core.document import (
    Category,
    Document,
    DocumentRepository,
)
from intranet.core.user import UserRepository
from intranet.core.user_details import UserDetailsRepository
from intranet.error import apology, login_required
from intranet.flask.dependable import Container

documents = Blueprint("documents", __name__)


@dataclass
class DocumentForm:
    dates: str
    dates_select: str
    date_range: str
    course_name: str
    course_price: str
    category: str


@documents.get("/documents")
@inject
@login_required
def documents_page(
    document_repository: DocumentRepository = Provide[Container.document_repository],
    users: UserRepository = Provide[Container.user_repository],
) -> str:
    is_admin = True if users.read(session["user_id"]).username == "admin" else False

    category_map = [(category.name, category.value) for category in Category]

    user_documents = (
        document_repository
        if is_admin
        else [
            item for item in document_repository if item.user_id == session["user_id"]
        ]
    )

    return render_template(
        "user_documents.html",
        documents=user_documents,
        categories=category_map,
        is_admin=is_admin,
    )


@documents.post("/update-document")
@inject
@login_required
def update_document(
    document_repository: DocumentRepository = Provide[Container.document_repository],
    users: UserRepository = Provide[Container.user_repository],
) -> Response | tuple[str, int]:
    is_admin = True if users.read(session["user_id"]).username == "admin" else False

    if is_admin:
        document_repository.update(
            request.form.get("document_id", ""),
            request.form.get("new_category", ""),
        )

    return redirect(url_for("documents.documents_page"))


@documents.get("/documents/<filename>")
@login_required
def pdf_viewer(filename: str) -> Response:
    return send_from_directory("../../documents", filename)


@documents.post("/documents")
@inject
@login_required
def create_document(
    details: UserDetailsRepository = Provide[Container.user_details_repository],
    document_repository: DocumentRepository = Provide[Container.document_repository],
) -> Response | tuple[str, int]:
    user = details.read(session["user_id"])

    form = DocumentForm(
        dates=request.form.get("dates", ""),
        dates_select=request.form.get("dates_select", ""),
        date_range=request.form.get("date_range", ""),
        course_name=request.form.get("course_name", ""),
        course_price=request.form.get("course_price", ""),
        category=request.form.get("category", ""),
    )

    if not user.first_name or not user.last_name:
        return apology("must fill user details", 403)

    document_id = str(uuid4())
    document = Document(
        id=document_id,
        user_id=session["user_id"],
        category=Category[form.category],
        directory=f"/documents/{document_id}.pdf",
        status="warning",
    )

    (
        GenerateDocument(language=str(os.getenv("DOC_LANGUAGE")))
        .with_id(document.id)
        .with_form(
            Category[form.category].name,
            form.dates,
            form.dates_select,
            form.date_range,
            form.course_name,
            form.course_price,
        )
        .with_name(user.first_name)
        .with_lastname(user.last_name)
        .with_layout(
            page_width=8.5 * inch,
            page_height=11 * inch,
            margin=50,
            line_height=18,
        )
    )

    document_repository.create(document)

    return redirect(url_for("documents.documents_page"))


@dataclass
class GenerateDocument:
    language: str
    id: str = ""
    body: str = ""
    first_name: str = ""
    last_name: str = ""

    @staticmethod
    def read_template(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def with_id(self, document_id: str) -> GenerateDocument:
        self.id = document_id

        return self

    def with_form(
        self,
        category: str,
        dates: str,
        dates_select: str,
        date_range: str,
        course_name: str,
        course_price: str,
    ) -> GenerateDocument:
        self.body = self.body_using(
            category,
            dates,
            dates_select,
            date_range,
            course_name,
            course_price,
        )

        return self

    def with_name(self, first_name: str) -> GenerateDocument:
        self.first_name = first_name

        return self

    def with_lastname(self, last_name: str) -> GenerateDocument:
        self.last_name = last_name

        return self

    def header(self) -> str:
        header = self.read_template(f"document_templates/head_{self.language}.txt")

        return header.replace("!<<FIRST_NAME>>", self.first_name).replace(
            "!<<LAST_NAME>>", self.last_name
        )

    def body_using(
        self,
        category: str,
        dates: str,
        dates_select: str,
        date_range: str,
        course_name: str,
        course_price: str,
    ) -> str:
        body_template = self.read_template(
            f"document_templates/{category}_body_{self.language}.txt"
        )

        return (
            body_template.replace("!<<DATE>>", dates)
            .replace("!<<DATE_SELECT>>", dates_select)
            .replace("!<<COURSE_DATE>>", date_range)
            .replace("!<<COURSE_NAME>>", course_name)
            .replace("!<<COURSE_PRICE>>", course_price)
        )

    def footer(self) -> str:
        footer = self.read_template(f"document_templates/foot_{self.language}.txt")

        return footer.replace("!<<FIRST_NAME>>", self.first_name).replace(
            "!<<LAST_NAME>>", self.last_name
        )

    def with_layout(
        self,
        page_width: float,
        page_height: float,
        margin: int,
        line_height: int,
    ) -> GenerateDocument:
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

        updated_text = self.header() + self.body + self.footer()

        with BytesIO() as buffer:
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("GeorgianFontNormal", 12)

            # Start from a reasonable position on the first page
            y = page_height - margin
            for line in updated_text.split("\n"):
                y = PdfConstructor(
                    page_width, page_height, margin, line_height
                ).draw_wrapped_text(line, pdf, y)
                if y < margin:
                    pdf.showPage()
                    pdf.setFont("GeorgianFontNormal", 12)
                    y = page_height - margin

            pdf.showPage()
            pdf.save()

            buffer.seek(0)
            with open(f"documents/{self.id}.pdf", "wb") as f:
                f.write(buffer.getvalue())

        return self


@dataclass
class PdfConstructor:
    page_width: float
    page_height: float
    margin: int
    line_height: int

    def draw_wrapped_text(
        self, line: str, pdf: canvas.Canvas, y_location: float
    ) -> float:
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
