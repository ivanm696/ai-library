# -*- coding: utf-8 -*-
"""Общий модуль для генерации PDF-книг библиотеки ИИ.

Шрифты DejaVu (с поддержкой кириллицы), единые стили, цветовая палитра
и функция build_book(), которая собирает готовый PDF с колонтитулами.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak,
    HRFlowable, ListFlowable, ListItem, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame

# ── Шрифты DejaVu (кириллица) ────────────────────────────────────────
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
if not os.path.isdir(FONT_DIR):
    # fallback — относительно файла (локальный копий шрифтов может не быть)
    FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

_FONTS = {
    "DejaVu":            "DejaVuSans.ttf",
    "DejaVu-Bold":       "DejaVuSans-Bold.ttf",
    "DejaVuMono":        "DejaVuSansMono.ttf",
    "DejaVuMono-Bold":   "DejaVuSansMono-Bold.ttf",
    "DejaVuSerif":       "DejaVuSerif.ttf",
    "DejaVuSerif-Bold":  "DejaVuSerif-Bold.ttf",
}
for _name, _file in _FONTS.items():
    try:
        pdfmetrics.registerFont(TTFont(_name, os.path.join(FONT_DIR, _file)))
    except Exception:
        pass

# ── Палитра ──────────────────────────────────────────────────────────
ACCENT          = colors.HexColor("#2563EB")   # синий — основной акцент
ACCENT_DARK     = colors.HexColor("#1E40AF")
LEVEL_BEGINNER  = colors.HexColor("#16A34A")   # зелёный
LEVEL_INTER     = colors.HexColor("#EA580C")   # оранжевый
LEVEL_ADVANCED  = colors.HexColor("#DC2626")   # красный
CODE_LN         = colors.HexColor("#E5E7EB")   # светло-серый для линий
INK             = colors.HexColor("#1F2937")   # тёмно-серый — основной текст
INK2            = colors.HexColor("#6B7280")   # серый — вторичный текст
PAPER           = colors.HexColor("#FFFFFF")
SOFT_BG         = colors.HexColor("#F3F4F6")   # светло-серый фон блоков
WARN_BG         = colors.HexColor("#FEF3C7")   # жёлтый фон для предупреждений
TIP_BG          = colors.HexColor("#DBEAFE")   # голубой фон для советов
DANGER_BG       = colors.HexColor("#FEE2E2")   # красный фон для предостережений

# ── Стили ────────────────────────────────────────────────────────────
def _build_styles():
    ss = getSampleStyleSheet()
    base = dict(fontName="DejaVu", fontSize=10.5, leading=15.5,
                textColor=INK, alignment=TA_JUSTIFY, spaceBefore=0, spaceAfter=4)
    S = {}
    S["Body"] = ParagraphStyle("Body", **base)
    S["BodyLeft"] = ParagraphStyle("BodyLeft", **{**base, "alignment": TA_LEFT})
    S["Small"] = ParagraphStyle("Small", parent=ss["Normal"],
        fontName="DejaVu", fontSize=8.5, leading=12, textColor=INK2)
    S["BookTitle"] = ParagraphStyle("BookTitle", parent=ss["Title"],
        fontName="DejaVu-Bold", fontSize=26, leading=32, textColor=ACCENT_DARK,
        alignment=TA_CENTER, spaceAfter=8)
    S["BookSubtitle"] = ParagraphStyle("BookSubtitle", parent=ss["Normal"],
        fontName="DejaVu", fontSize=12, leading=16, textColor=INK2,
        alignment=TA_CENTER, spaceAfter=10)
    S["Cover"] = ParagraphStyle("Cover", parent=ss["Normal"],
        fontName="DejaVu", fontSize=10, leading=14, textColor=INK2,
        alignment=TA_CENTER)
    S["H1"] = ParagraphStyle("H1", parent=ss["Heading1"],
        fontName="DejaVu-Bold", fontSize=18, leading=24, textColor=ACCENT_DARK,
        spaceBefore=16, spaceAfter=8, alignment=TA_LEFT)
    S["H2"] = ParagraphStyle("H2", parent=ss["Heading2"],
        fontName="DejaVu-Bold", fontSize=14, leading=18, textColor=ACCENT,
        spaceBefore=12, spaceAfter=6, alignment=TA_LEFT)
    S["H3"] = ParagraphStyle("H3", parent=ss["Heading3"],
        fontName="DejaVu-Bold", fontSize=11.5, leading=15, textColor=INK,
        spaceBefore=8, spaceAfter=4, alignment=TA_LEFT)
    S["Code"] = ParagraphStyle("Code", parent=ss["Code"],
        fontName="DejaVuMono", fontSize=8.5, leading=12, textColor=INK,
        backColor=SOFT_BG, borderColor=CODE_LN, borderWidth=0.5,
        borderPadding=6, leftIndent=4, rightIndent=4, spaceBefore=4, spaceAfter=8)
    S["Quote"] = ParagraphStyle("Quote", parent=ss["Normal"],
        fontName="DejaVuSerif", fontSize=10.5, leading=15.5, textColor=INK2,
        leftIndent=14, rightIndent=14, spaceBefore=6, spaceAfter=6,
        alignment=TA_LEFT, borderPadding=4)
    S["Caption"] = ParagraphStyle("Caption", parent=ss["Normal"],
        fontName="DejaVu", fontSize=8.5, leading=11, textColor=INK2,
        alignment=TA_CENTER, spaceAfter=6)
    S["White"] = ParagraphStyle("White", parent=ss["Normal"],
        fontName="DejaVu", fontSize=10, leading=14, textColor=colors.white)
    S["WhiteBold"] = ParagraphStyle("WhiteBold", parent=ss["Normal"],
        fontName="DejaVu-Bold", fontSize=11, leading=15, textColor=colors.white)
    return S

STYLES = _build_styles()
S = STYLES  # short alias for convenience

# ── Уровни ───────────────────────────────────────────────────────────
LEVEL_LABELS = {
    LEVEL_BEGINNER:  ("Начинающий", "#16A34A"),
    LEVEL_INTER:     ("Средний",    "#EA580C"),
    LEVEL_ADVANCED:  ("Продвинутый","#DC2626"),
}

def level_badge(label, color):
    """Возвращает Table с цветным бейджем уровня."""
    t = Table([[Paragraph(
        f'<font name="DejaVu-Bold" size="8" color="white">{label}</font>',
        STYLES["White"])]], colWidths=[32 * mm], rowHeights=[8 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return t

# ── Хелперы для контента ─────────────────────────────────────────────

def wrap_cells(rows):
    """Оборачивает строковые ячейки таблицы в Paragraph."""
    result = []
    for row in rows:
        new_row = []
        for cell in row:
            if isinstance(cell, str):
                new_row.append(Paragraph(cell, STYLES["Small"]))
            else:
                new_row.append(cell)
        result.append(new_row)
    return result


def code_block(text):
    """Блок кода с моноширинным шрифтом."""
    escaped = (text.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;"))
    lines = escaped.split("\n")
    html = "<br/>".join(lines)
    return Paragraph(html, STYLES["Code"])


def bullet_list(items, style=None):
    """Маркированный список."""
    style = style or STYLES["Body"]
    items_flow = [ListItem(Paragraph(item, style), leftIndent=6,
                           value="bullet", bulletColor=ACCENT)
                  for item in items]
    return ListFlowable(items_flow, bulletType="bullet", start="•",
                        bulletFontSize=8, leftIndent=14, bulletOffsetY=-1)


def numbered_list(items, style=None):
    """Нумерованный список."""
    style = style or STYLES["Body"]
    items_flow = [ListItem(Paragraph(item, style), leftIndent=6)
                  for item in items]
    return ListFlowable(items_flow, bulletType="1", bulletFormat="%s.",
                        leftIndent=18, bulletFontSize=10)


def callout(title, text, bg_color=TIP_BG, icon="💡"):
    """Цветной блок-выноска (совет, предупреждение, предостережение)."""
    inner = Table([[
        Paragraph(f'<font name="DejaVu-Bold" size="10">{icon} {title}</font>',
                  STYLES["BodyLeft"]),
    ], [
        Paragraph(text, STYLES["BodyLeft"]),
    ]], colWidths=[160 * mm])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), 0.5, CODE_LN),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, 0), 0.3, CODE_LN),
    ]))
    return KeepTogether([Spacer(1, 3 * mm), inner, Spacer(1, 3 * mm)])


def key_takeaways(items):
    """Блок «Ключевые выводы» в конце главы."""
    rows = [[Paragraph(
        '<font name="DejaVu-Bold" color="white" size="11">Ключевые выводы</font>',
        STYLES["WhiteBold"])]]
    for item in items:
        rows.append([Paragraph(f"• {item}", STYLES["BodyLeft"])])
    t = Table(rows, colWidths=[160 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("BACKGROUND", (0, 1), (-1, -1), SOFT_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, CODE_LN),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return KeepTogether([Spacer(1, 4 * mm), t, Spacer(1, 4 * mm)])


def chapter_header(num, title, subtitle="", level_color=ACCENT):
    """Заголовок главы: номер в круге + название."""
    num_para = Paragraph(
        f'<font name="DejaVu-Bold" size="9" color="white">{num}</font>',
        STYLES["WhiteBold"])
    circle = Table([[num_para]], colWidths=[12 * mm], rowHeights=[12 * mm])
    circle.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), level_color),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    title_block = Table([
        [circle, Paragraph(title, STYLES["H1"])],
        ["", Paragraph(subtitle, STYLES["Small"]) if subtitle else ""],
    ], colWidths=[16 * mm, 150 * mm])
    title_block.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("SPAN", (0, 0), (0, 1)),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return KeepTogether([
        title_block,
        Spacer(1, 2 * mm),
        HRFlowable(width="100%", thickness=0.8, color=CODE_LN, spaceAfter=8),
    ])


def two_col_table(rows, col_widths=None, header=True):
    """Простая таблица с шапкой."""
    cw = col_widths or [80 * mm, 80 * mm]
    t = Table(wrap_cells(rows), colWidths=cw)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.4, CODE_LN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
        ]
    t.setStyle(TableStyle(style))
    return t


# ── Документ с колонтитулами ─────────────────────────────────────────

class _BookDoc(BaseDocTemplate):
    """DocTemplate с верхним и нижним колонтитулами."""

    def __init__(self, filename, book_title, footer_label, **kw):
        self._book_title = book_title
        self._footer_label = footer_label
        BaseDocTemplate.__init__(self, filename, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin,
                      self.width, self.height, id="main")
        self.addPageTemplates([
            PageTemplate(id="book", frames=[frame], onPage=self._draw_decor)
        ])

    def _draw_decor(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        # верхняя полоса
        canvas.setFillColor(ACCENT)
        canvas.rect(0, h - 12 * mm, w, 12 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("DejaVu", 8)
        canvas.drawString(20 * mm, h - 8 * mm, self._book_title)
        canvas.drawRightString(w - 20 * mm, h - 8 * mm, self._footer_label)
        # нижний колонтитул
        canvas.setStrokeColor(CODE_LN)
        canvas.setLineWidth(0.4)
        canvas.line(20 * mm, 14 * mm, w - 20 * mm, 14 * mm)
        canvas.setFillColor(INK2)
        canvas.setFont("DejaVu", 8)
        canvas.drawString(20 * mm, 9 * mm, "Библиотека ИИ")
        canvas.drawRightString(w - 20 * mm, 9 * mm, f"Стр. {doc.page}")
        canvas.restoreState()


def build_book(filename, series_title, book_title, book_code, story,
               footer_label, output_dir=None):
    """Собирает PDF из story (список Flowable)."""
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, filename)
    doc = _BookDoc(
        filename, series_title, footer_label,
        pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=f"{series_title} — {book_title}",
        author="Библиотека ИИ",
    )
    doc.build(story)
    print(f"  ✓ {filename}")
    return filename
