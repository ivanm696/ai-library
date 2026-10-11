# -*- coding: utf-8 -*-
"""Каталог: Библиотека ИИ — обзор всех 5 книг."""

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.units import mm
from reportlab.lib import colors
from book_engine import (
    STYLES as S, build_book, wrap_cells,
    LEVEL_BEGINNER, LEVEL_INTER, LEVEL_ADVANCED, ACCENT, CODE_LN, INK2,
)

story = []
story.append(Spacer(1, 40 * mm))
story.append(Paragraph("Библиотека ИИ", S["BookTitle"]))
story.append(Paragraph(
    "Независимая обучающая библиотека об искусственном интеллекте — от первых понятий до архитектуры "
    "трансформеров, практики и этики. 5 книг, все уровни и категории в одной серии.", S["BookSubtitle"]))
story.append(Spacer(1, 6 * mm))
story.append(HRFlowable(width="40%", thickness=1.2, color=ACCENT, spaceAfter=6, hAlign="CENTER"))
story.append(Paragraph("Уровень: Начинающий — Продвинутый · 5 книг", S["Cover"]))
story.append(PageBreak())

story.append(Paragraph("Состав библиотеки", S["H1"]))
story.append(Paragraph(
    "Каждая книга читается самостоятельно, но вместе они образуют полный путь: от понимания того, "
    "что такое ИИ вообще, до того, как он устроен внутри, как с ним работать на практике и какие "
    "вопросы он поднимает для общества.", S["Body"]))

catalog = Table(wrap_cells([
    ["№", "Книга", "О чём", "Уровень"],
    ["1", "Основы искусственного интеллекта",
     "Что такое ИИ, история, машинное обучение, нейросети и LLM простыми словами, мифы об ИИ",
     "Начинающий"],
    ["2", "Промпт-инжиниринг",
     "Как формулировать запросы: от базовых принципов до few-shot, Chain-of-Thought и структурированного вывода",
     "Начинающий — Продвинутый"],
    ["3", "Архитектура нейросетей и трансформеров",
     "Нейрон, обратное распространение, механизм внимания, токенизация, RLHF, законы масштабирования",
     "Средний — Продвинутый"],
    ["4", "Практическое применение ИИ",
     "Инструменты, API, агенты, RAG, автоматизация рабочих процессов и безопасная интеграция",
     "Начинающий — Продвинутый"],
    ["5", "Этика, безопасность и ограничения ИИ",
     "Предвзятость, приватность, дезинформация, AI safety, регулирование, ответственное использование",
     "Начинающий — Продвинутый"],
]), colWidths=[10 * mm, 48 * mm, 78 * mm, 34 * mm])
catalog.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.3),
    ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
    ("TEXTCOLOR", (0, 0), (-1, 0), "white"),
    ("GRID", (0, 0), (-1, -1), 0.5, CODE_LN),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
]))
story.append(catalog)
story.append(Spacer(1, 8 * mm))

story.append(Paragraph("Как читать библиотеку", S["H2"]))
story.append(Paragraph(
    "Если вы только начинаете — читайте по порядку: Книга 1 даёт общую карту понятий, Книга 2 сразу "
    "даёт практический навык работы с ИИ, Книга 4 показывает, как применять это в инструментах и "
    "автоматизации, а Книга 5 — на что обращать внимание с точки зрения рисков и ответственности. "
    "Книга 3 — для тех, кто хочет понять техническую «начинку» языковых моделей; её можно читать "
    "в любой момент, отдельно от остальных.", S["Body"]))

story.append(Paragraph("Обозначения уровней", S["H2"]))
from book_engine import level_badge
levels_row = Table([[
    level_badge("Начинающий", LEVEL_BEGINNER),
    Paragraph("базовые понятия, без предварительных знаний", S["Small"]),
]], colWidths=[36 * mm, 120 * mm])
levels_row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
story.append(levels_row)
story.append(Spacer(1, 2 * mm))
levels_row2 = Table([[
    level_badge("Средний", LEVEL_INTER),
    Paragraph("требует понимания основ, подходит для уверенных пользователей", S["Small"]),
]], colWidths=[36 * mm, 120 * mm])
levels_row2.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
story.append(levels_row2)
story.append(Spacer(1, 2 * mm))
levels_row3 = Table([[
    level_badge("Продвинутый", LEVEL_ADVANCED),
    Paragraph("техническая глубина, ориентировано на разработчиков и исследователей", S["Small"]),
]], colWidths=[36 * mm, 120 * mm])
levels_row3.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
story.append(levels_row3)

build_book(
    "Kniga-0-Katalog-Biblioteki.pdf",
    "Библиотека ИИ",
    "Каталог",
    "K0",
    story,
    "Библиотека ИИ · Каталог",
)
print("Каталог построен.")
