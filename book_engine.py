# -*- coding: utf-8 -*-
"""
Общий движок для серии книг «Библиотека ИИ» (5 книг).
Регистрирует шрифты DejaVu (полная поддержка кириллицы), задаёт стили,
и даёт вспомогательные функции: code_block, note_block, level_badge,
h_section, cover_page, PageNumCanvas, build_book.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem, PageBreak
)
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ----------------------------------------------------------------------
# Шрифты
# ----------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Oblique", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-BoldOblique", os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuMono", os.path.join(FONT_DIR, "DejaVuSansMono.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuMono-Bold", os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")))
pdfmetrics.registerFontFamily(
    "DejaVu", normal="DejaVu", bold="DejaVu-Bold",
    italic="DejaVu-Oblique", boldItalic="DejaVu-BoldOblique",
)

# ----------------------------------------------------------------------
# Палитра
# ----------------------------------------------------------------------
INK = colors.HexColor("#1a1a2e")
INK2 = colors.HexColor("#4a4a68")
ACCENT = colors.HexColor("#5b3cc4")
ACCENT2 = colors.HexColor("#1f8a70")
CODE_BG = colors.HexColor("#f4f2fb")
CODE_LN = colors.HexColor("#d9d2f0")
NOTE_BG = colors.HexColor("#fff6e0")
NOTE_LN = colors.HexColor("#f0dca0")

LEVEL_BEGINNER = colors.HexColor("#1f8a70")
LEVEL_INTER = colors.HexColor("#c47f17")
LEVEL_ADVANCED = colors.HexColor("#c43c3c")


def make_styles():
    """Return a fresh mapping of named paragraph styles for the book series."""
    S = {}
    S["BookTitle"] = ParagraphStyle(
        "BookTitle", fontName="DejaVu-Bold", fontSize=30, leading=36,
        textColor=INK, alignment=TA_CENTER, spaceAfter=10,
    )
    S["BookSubtitle"] = ParagraphStyle(
        "BookSubtitle", fontName="DejaVu-Oblique", fontSize=15, leading=20,
        textColor=INK2, alignment=TA_CENTER, spaceAfter=18,
    )
    S["VolTag"] = ParagraphStyle(
        "VolTag", fontName="DejaVu-Bold", fontSize=12, leading=14,
        textColor=colors.white, alignment=TA_CENTER,
    )
    S["Cover"] = ParagraphStyle(
        "Cover", fontName="DejaVu", fontSize=12, leading=16,
        textColor=INK2, alignment=TA_CENTER,
    )
    S["H1"] = ParagraphStyle(
        "H1", fontName="DejaVu-Bold", fontSize=18, leading=22,
        textColor=ACCENT, spaceBefore=18, spaceAfter=10,
    )
    S["H2"] = ParagraphStyle(
        "H2", fontName="DejaVu-Bold", fontSize=13, leading=17,
        textColor=INK, spaceBefore=12, spaceAfter=6,
    )
    S["H3"] = ParagraphStyle(
        "H3", fontName="DejaVu-Bold", fontSize=11.5, leading=15,
        textColor=ACCENT2, spaceBefore=8, spaceAfter=4,
    )
    S["Body"] = ParagraphStyle(
        "Body", fontName="DejaVu", fontSize=10.5, leading=15.5,
        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
    )
    S["Bullet"] = ParagraphStyle(
        "Bullet", fontName="DejaVu", fontSize=10.5, leading=15,
        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=3, leftIndent=4,
    )
    S["Code"] = ParagraphStyle(
        "Code", fontName="DejaVuMono", fontSize=8.7, leading=12.5,
        textColor=INK, backColor=CODE_BG,
        borderPadding=(8, 8, 8, 8), borderWidth=0.75, borderColor=CODE_LN,
        spaceBefore=6, spaceAfter=10,
    )
    S["Note"] = ParagraphStyle(
        "Note", fontName="DejaVu", fontSize=9.7, leading=13.5,
        textColor=INK, backColor=NOTE_BG,
        borderPadding=(8, 8, 8, 8), borderWidth=0.75, borderColor=NOTE_LN,
        spaceBefore=6, spaceAfter=10,
    )
    S["TocEntry"] = ParagraphStyle(
        "TocEntry", fontName="DejaVu", fontSize=10.5, leading=16,
        textColor=INK,
    )
    S["TocH1"] = ParagraphStyle(
        "TocH1", fontName="DejaVu-Bold", fontSize=12.5, leading=18,
        textColor=ACCENT, spaceBefore=10,
    )
    S["Small"] = ParagraphStyle(
        "Small", fontName="DejaVu", fontSize=8.5, leading=11,
        textColor=INK2,
    )
    S["Cell"] = ParagraphStyle(
        "Cell", fontName="DejaVu", fontSize=8.5, leading=11.5,
        textColor=INK,
    )
    S["CellHead"] = ParagraphStyle(
        "CellHead", fontName="DejaVu-Bold", fontSize=8.5, leading=11.5,
        textColor=colors.white,
    )
    return S


# ----------------------------------------------------------------------
# Вспомогательные блоки
# ----------------------------------------------------------------------

def level_badge(text, color):
    """Return a 32 by 6.5 mm badge with white text on a ``color`` background."""
    t = Table([[text]], colWidths=[32 * mm], rowHeights=[6.5 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def code_block(code_text, style=None):
    """Return a code paragraph preserving line breaks and leading spaces.

    Escape ``&``, ``<``, and ``>`` so code is rendered as literal text.
    Use the shared Code style unless a truthy ``style`` is supplied.
    """
    lines = []
    for ln in code_text.split("\n"):
        stripped = ln.lstrip(" ")
        indent = len(ln) - len(stripped)
        safe = (
            stripped.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        lines.append("&nbsp;" * indent + safe)
    return Paragraph("<br/>".join(lines), style or _STYLES["Code"])


def wrap_cells(rows):
    """Return new rows of wrapping paragraphs, converting each cell to text.

    The first row uses bold white header text; later rows use body cell text.
    Set background colors on the enclosing table. Cell text is parsed as
    ReportLab paragraph markup; malformed markup can raise ValueError.
    Empty input returns an empty list.
    """
    out = []
    for i, row in enumerate(rows):
        style = _STYLES["CellHead"] if i == 0 else _STYLES["Cell"]
        out.append([Paragraph(str(c), style) for c in row])
    return out


def note_block(text, label="Примечание"):
    """Return a note paragraph prefixed by a bold ``label`` and a period.

    ``text`` and ``label`` accept ReportLab paragraph markup without escaping.
    Malformed markup can raise ValueError.
    """
    return Paragraph(f"<b>{label}.</b> {text}", _STYLES["Note"])


def h_section(number, title, level_color=None, level_text=None):
    """Return a numbered heading, optionally paired with a level badge.

    With ``level_color=None``, return a paragraph and ignore ``level_text``.
    Otherwise, return a table using ``level_text`` and ``level_color`` for
    the badge. The heading accepts ReportLab paragraph markup; malformed
    markup can raise ValueError.
    """
    if level_color is None:
        return Paragraph(f"{number}. {title}", _STYLES["H1"])
    left = Paragraph(f"{number}. {title}", _STYLES["H1"])
    right = level_badge(level_text, level_color)
    t = Table([[left, right]], colWidths=[132 * mm, 34 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def cover_page(vol_num, vol_tag, title, subtitle, level_range, color):
    """Return cover flowables ending with a page break.

    ``vol_num`` labels the volume, ``color`` colors its badge and divider,
    and ``level_range`` is the displayed reading level. ``vol_tag`` is unused.
    Title, subtitle, and level text accept ReportLab paragraph markup;
    malformed markup can raise ValueError.
    """
    flow = []
    flow.append(Spacer(1, 55 * mm))
    tag_table = Table([[f"КНИГА {vol_num}"]], colWidths=[40 * mm], rowHeights=[9 * mm])
    tag_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    centered = Table([[tag_table]], colWidths=[170 * mm])
    centered.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    flow.append(centered)
    flow.append(Spacer(1, 10 * mm))
    flow.append(Paragraph(title, _STYLES["BookTitle"]))
    flow.append(Paragraph(subtitle, _STYLES["BookSubtitle"]))
    flow.append(Spacer(1, 6 * mm))
    flow.append(HRFlowable(width="40%", thickness=1.2, color=color, spaceAfter=6, hAlign="CENTER"))
    flow.append(Paragraph(f"Уровень: {level_range}", _STYLES["Cover"]))
    flow.append(Paragraph("Библиотека ИИ · 5 книг · все уровни и категории", _STYLES["Cover"]))
    flow.append(PageBreak())
    return flow


class PageNumCanvas(pdfcanvas.Canvas):
    book_short_tag = ""

    def __init__(self, *args, **kwargs):
        """Initialize a ReportLab canvas with an empty queue of completed pages."""
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        """Queue the current page and start a new one, deferring PDF output."""
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Write pages queued by ``showPage`` to the PDF, adding footers.

        The final page must be queued before calling this method. Output
        OSError exceptions and RuntimeError from saving more than once
        propagate to the caller.
        """
        num_pages = len(self._saved_page_states)
        for i, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self.draw_footer(i + 1, num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_num, total_pages):
        """Draw the book tag and page number, leaving page 1 without a footer.

        ``page_num`` counts from 1, including the cover; ``total_pages`` is unused.
        The footer uses fixed A4 coordinates and changes the canvas drawing state.
        """
        if page_num == 1:
            return
        self.setStrokeColor(CODE_LN)
        self.setLineWidth(0.5)
        self.line(20 * mm, 16 * mm, 190 * mm, 16 * mm)
        self.setFont("DejaVu", 8)
        self.setFillColor(INK2)
        self.drawString(20 * mm, 11 * mm, self.book_short_tag)
        self.drawRightString(190 * mm, 11 * mm, f"стр. {page_num}")


def make_canvas_factory(book_short_tag):
    """Return a PageNumCanvas subclass using ``book_short_tag`` in its footers."""
    class _Canvas(PageNumCanvas):
        pass
    _Canvas.book_short_tag = book_short_tag
    return _Canvas


def build_book(filename, title, subtitle, vol_tag, story, book_short_tag):
    """Write ``story`` to an A4 PDF with book footers and ``title`` metadata.

    ``filename`` is an output filename or writable binary stream. Building
    consumes the mutable flowable list ``story``. ``book_short_tag`` appears
    in footers after the cover; ``subtitle`` and ``vol_tag`` are unused.
    ReportLab LayoutError and output OSError exceptions propagate to callers.
    """
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        topMargin=18 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
        title=title, author="Библиотека ИИ",
    )
    canvas_cls = make_canvas_factory(book_short_tag)
    doc.build(story, canvasmaker=canvas_cls)


_STYLES = make_styles()
STYLES = _STYLES
