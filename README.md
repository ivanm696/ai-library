# ai-library
# Библиотека ИИ

Независимая обучающая библиотека об искусственном интеллекте — 5 книг в формате PDF,
покрывающих все уровни (от новичка до продвинутого) и категории (теория, практика, этика)
в одной связной серии.

Все книги сгенерированы из Python-скриптов (ReportLab) с полной поддержкой кириллицы
(шрифты DejaVu Sans), единым визуальным стилем, цветными бейджами уровня сложности для
каждого раздела и автоматической нумерацией страниц.

## Состав библиотеки

| № | Книга | Файл | О чём | Уровень |
|---|---|---|---|---|
| — | **Каталог** | [`Kniga-0-Katalog-Biblioteki.pdf`](pdf/Kniga-0-Katalog-Biblioteki.pdf) | Обзор всей серии, порядок чтения, обозначения уровней | Базовый |
| 1 | **Основы искусственного интеллекта** | [`Kniga-1-Osnovy-Iskusstvennogo-Intellekta.pdf`](pdf/Kniga-1-Osnovy-Iskusstvennogo-Intellekta.pdf) | Что такое ИИ, краткая история, машинное обучение, нейросети | Базовый |
| 2 | **Промпт-инжиниринг** | [`Kniga-2-Prompt-Inzhiniring.pdf`](pdf/Kniga-2-Prompt-Inzhiniring.pdf) | Базовые принципы, zero/few-shot, Chain-of-Thought, системный промптинг | Базовый |
| 3 | **Архитектура нейросетей и трансформеров** | [`Kniga-3-Arkhitektura-Neirosetey-i-Transformerov.pdf`](pdf/Kniga-3-Arkhitektura-Neirosetey-i-Transformerov.pdf) | Нейрон, архитектуры, трансформеры, обучение и масштабирование | Продвинутый |
| 4 | **Практическое применение ИИ** | [`Kniga-4-Prakticheskoe-Primenenie-II.pdf`](pdf/Kniga-4-Prakticheskoe-Primenenie-II.pdf) | Карта инструментов, API, автоматизация, рабочие сценарии | Практический |
| 5 | **Этика, безопасность и ограничения ИИ** | [`Kniga-5-Etika-Bezopasnost-i-Ogranicheniya-II.pdf`](pdf/Kniga-5-Etika-Bezopasnost-i-Ogranicheniya-II.pdf) | Предвзятость, приватность, риски, ответственность, ограничения | Все уровни |

## Как читать

Каждая книга самодостаточна, но вместе они образуют полный путь:

1. **Книга 1** — общая карта понятий, без предварительных знаний.
2. **Книга 2** — практический навык работы с ИИ прямо сейчас.
3. **Книга 4** — как применять это в инструментах, API и автоматизации.
4. **Книга 5** — на что обращать внимание с точки зрения рисков и ответственности.
5. **Книга 3** — техническая «начинка» языковых моделей; можно читать в любой момент отдельно.

## Структура репозитория

```
book_engine.py        — общий движок (шрифты, стили, таблицы, обложки, футер/нумерация страниц)
book0_catalog.py      -> pdf/Kniga-0-Katalog-Biblioteki.pdf
book1_fundamentals.py -> pdf/Kniga-1-Osnovy-Iskusstvennogo-Intellekta.pdf
book2_prompting.py    -> pdf/Kniga-2-Prompt-Inzhiniring.pdf
book3_architecture.py -> pdf/Kniga-3-Arkhitektura-Neirosetey-i-Transformerov.pdf
book4_practice.py     -> pdf/Kniga-4-Prakticheskoe-Primenenie-II.pdf
book5_ethics.py       -> pdf/Kniga-5-Etika-Bezopasnost-i-Ogranicheniya-II.pdf
```

## Пересборка PDF локально

```bash
pip install reportlab
python3 book0_catalog.py
python3 book1_fundamentals.py
python3 book2_prompting.py
python3 book3_architecture.py
python3 book4_practice.py
python3 book5_ethics.py
```

Требуются системные шрифты DejaVu Sans (`DejaVuSans.ttf`, `-Bold`, `-Oblique`,
`DejaVuSansMono[-Bold]`) — на Debian/Ubuntu: `apt install fonts-dejavu`.

## Лицензия

Контент создан для свободного личного и образовательного использования.
