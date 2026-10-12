# -*- coding: utf-8 -*-
"""Книга 4: Практическое применение ИИ.

Инструменты, API, агенты, RAG, автоматизация рабочих процессов
и безопасная интеграция.
"""
from reportlab.platypus import Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.lib.units import mm
from book_engine import (
    S, build_book, chapter_header, bullet_list, numbered_list,
    callout, key_takeaways, code_block, two_col_table, level_badge,
    LEVEL_BEGINNER, LEVEL_INTER, LEVEL_ADVANCED, ACCENT, CODE_LN,
)

story = []

# ── Обложка ──────────────────────────────────────────────────────────
story.append(Spacer(1, 50 * mm))
story.append(Paragraph("Книга 4", S["Cover"]))
story.append(Spacer(1, 4 * mm))
story.append(Paragraph("Практическое применение ИИ", S["BookTitle"]))
story.append(Paragraph(
    "Инструменты, API, агенты, RAG, автоматизация рабочих процессов "
    "и безопасная интеграция", S["BookSubtitle"]))
story.append(Spacer(1, 6 * mm))
story.append(HRFlowable(width="40%", thickness=1.2, color=ACCENT,
                        spaceAfter=6, hAlign="CENTER"))
story.append(level_badge("Начинающий — Продвинутый", LEVEL_INTER))
story.append(Spacer(1, 60 * mm))
story.append(Paragraph("Библиотека ИИ · Книга 4 из 5", S["Cover"]))
story.append(PageBreak())

# ── Оглавление ───────────────────────────────────────────────────────
story.append(Paragraph("Содержание", S["H1"]))
story.append(HRFlowable(width="100%", thickness=0.5, color=CODE_LN, spaceAfter=8))
toc = [
    "1. Карта инструментов: что существует и для чего",
    "2. Работа с API языковых моделей",
    "3. RAG: поиск + генерация",
    "4. ИИ-агенты: автономные действия",
    "5. Автоматизация рабочих процессов",
    "6. ИИ для контента: текст, изображения, видео",
    "7. ИИ в разработке ПО",
    "8. ИИ в бизнесе и аналитике",
    "9. Безопасная интеграция: что проверять",
    "10. Практикум: строим RAG-систему",
]
story.append(numbered_list(toc))
story.append(PageBreak())

# ── Глава 1 ──────────────────────────────────────────────────────────
story.append(chapter_header("1", "Карта инструментов",
    "Что существует и для чего",
    level_color=LEVEL_BEGINNER))

story.append(Paragraph(
    "Современный ИИ — это не одна программа, а целая экосистема "
    "инструментов. Важно понимать, какой инструмент для какой задачи.",
    S["Body"]))

story.append(two_col_table([
    ["Категория", "Примеры", "Для чего"],
    ["Чат-модели (LLM)", "ChatGPT, Claude, Gemini, Copilot", "Текст, диалоги, анализ, код"],
    ["Генерация изображений", "Midjourney, DALL-E, Stable Diffusion", "Иллюстрации, дизайн, арт"],
    ["Генерация видео", "Sora, Runway, Pika", "Видеоконтент, анимация"],
    ["Генерация аудио", "ElevenLabs, Suno", "Озвучка, музыка"],
    ["Транскрипция", "Whisper, Otter.ai", "Речь → текст, субтитры"],
    ["Перевод", "DeepL, Google Translate", "Перевод с сохранением контекста"],
    ["Поиск + ИИ", "Perplexity, Bing Chat", "Поиск с генеративным ответом"],
    ["Программирование", "GitHub Copilot, Cursor, Codeium", "Автодополнение, рефакторинг"],
    ["Специализированные", "AlphaFold, RoseTTAFold", "Наука, медицина, биология"],
], col_widths=[38 * mm, 58 * mm, 64 * mm]))

story.append(callout(
    "Главный принцип выбора",
    "Не ищите «лучший ИИ вообще». Ищите лучший инструмент для конкретной "
    "задачи. Для перевода лучше DeepL, для написания кода — Copilot, "
    "для рассуждений — Claude, для изображений — Midjourney.",
    bg_color=__import__("book_engine").TIP_BG, icon="🎯"))

story.append(key_takeaways([
    "ИИ-инструменты делятся на категории по типу задачи",
    "Нет «лучшего ИИ вообще» — есть лучший для конкретной задачи",
    "Многие задачи решаются связкой нескольких инструментов",
]))
story.append(PageBreak())

# ── Глава 2 ──────────────────────────────────────────────────────────
story.append(chapter_header("2", "Работа с API языковых моделей",
    "Как подключить ИИ к своему приложению",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "API позволяет отправлять промпты к языковой модели программно и "
    "получать ответ в коде. Это основа любой ИИ-интеграции.", S["Body"]))

story.append(Paragraph("Пример: вызов OpenAI API (Python)", S["H2"]))
story.append(code_block(
    "from openai import OpenAI\n"
    "\n"
    "client = OpenAI(api_key=\"sk-...\")\n"
    "\n"
    "response = client.chat.completions.create(\n"
    "    model=\"gpt-4o\",\n"
    "    messages=[\n"
    "        {\"role\": \"system\", \"content\": \"Ты — помощник-переводчик.\"},\n"
    "        {\"role\": \"user\", \"content\": \"Переведи на английский: Привет, мир!\"},\n"
    "    ],\n"
    "    temperature=0.7,\n"
    "    max_tokens=100\n"
    ")\n"
    "\n"
    "print(response.choices[0].message.content)\n"
    "# → \"Hello, world!\""))

story.append(Paragraph("Ключевые параметры API", S["H2"]))
story.append(two_col_table([
    ["Параметр", "Что делает", "Типичные значения"],
    ["model", "Какую модель использовать", "gpt-4o, claude-3.5-sonnet, gemini-pro"],
    ["temperature", "Креативность (0 = точно, 1 = разнообразно)", "0.0 — 1.0"],
    ["max_tokens", "Максимум токенов в ответе", "100 — 4096"],
    ["top_p", "Ограничение выбора токенов (nucleus sampling)", "0.9 — 1.0"],
    ["stream", "Ответ по частям (streaming)", "True / False"],
    ["messages", "История диалога с ролями", "system / user / assistant"],
], col_widths=[30 * mm, 70 * mm, 60 * mm]))

story.append(Paragraph("Streaming — зачем и как", S["H2"]))
story.append(Paragraph(
    "Streaming позволяет получать ответ по частям, как только модель "
    "генерирует токены. Это даёт эффект «печатающего» ответа и снижает "
    "воспринимаемое время ожидания.", S["Body"]))
story.append(code_block(
    "stream = client.chat.completions.create(\n"
    "    model=\"gpt-4o\",\n"
    "    messages=[{\"role\": \"user\", \"content\": \"Расскажи сказку\"}],\n"
    "    stream=True,\n"
    ")\n"
    "\n"
    "for chunk in stream:\n"
    "    if chunk.choices[0].delta.content:\n"
    "        print(chunk.choices[0].delta.content, end=\"\")"))

story.append(callout(
    "Стоимость",
    "API тарифицируется по токенам: отдельно входные (prompt tokens) "
    "и выходные (completion tokens). Входные дешевле. Контекст в "
    "сообщениях тоже считается. Длинный диалог может стоить дороже, "
    "чем вы ожидаете.",
    bg_color=__import__("book_engine").WARN_BG, icon="💰"))

story.append(key_takeaways([
    "API = программный доступ к языковой модели",
    "Ключевые параметры: model, temperature, max_tokens, messages",
    "Streaming даёт ответ по частям — лучше UX",
    "Стоимость зависит от количества токенов (вход + выход)",
]))
story.append(PageBreak())

# ── Глава 3 ──────────────────────────────────────────────────────────
story.append(chapter_header("3", "RAG: поиск + генерация",
    "Retrieval-Augmented Generation",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "RAG — это техника, при которой модель перед ответом ищет информацию "
    "в вашей базе знаний. Это решает две проблемы: галлюцинации и "
    "устаревшие знания модели.", S["Body"]))

story.append(Paragraph("Как работает RAG", S["H2"]))
story.append(numbered_list([
    "Документы разбиваются на куски (chunks) по 200-1000 токенов",
    "Каждый кусок превращается в embedding-вектор и сохраняется в "
    "векторной базе данных",
    "При запросе пользователя: запрос тоже превращается в вектор",
    "Векторная база находит ближайшие (cosine similarity) куски документов",
    "Найденные куски + исходный запрос отправляются в LLM",
    "LLM генерирует ответ на основе найденного контекста",
]))

story.append(code_block(
    "Схема RAG:\n"
    "\n"
    "  Документы → chunks → embeddings → векторная БД\n"
    "                                              ↑\n"
    "  Запрос → embedding → поиск ближайших → context\n"
    "                                              ↓\n"
    "  Промпт = [context + запрос] → LLM → ответ с цитатами"))

story.append(Paragraph("Компоненты RAG-системы", S["H2"]))
story.append(two_col_table([
    ["Компонент", "Примеры", "Задача"],
    ["Embedding-модель", "text-embedding-3-small, BGE, E5", "Текст → вектор"],
    ["Векторная БД", "Pinecone, Weaviate, Qdrant, pgvector", "Хранение и поиск по сходству"],
    ["LLM", "GPT-4o, Claude, LLaMA", "Генерация ответа по контексту"],
    ["Фреймворк", "LangChain, LlamaIndex", "Оркестрация пайплайна"],
], col_widths=[36 * mm, 64 * mm, 60 * mm]))

story.append(callout(
    "Когда RAG лучше fine-tuning",
    "Если данные часто меняются (документация, база знаний, новости) — "
    "RAG лучше. Fine-tuning нужен, когда меняется стиль или поведение "
    "модели, а не факты. Часто их комбинируют.",
    bg_color=__import__("book_engine").TIP_BG, icon="📚"))

story.append(key_takeaways([
    "RAG = поиск по базе знаний + генерация ответа",
    "Решает галлюцинации и устаревание знаний",
    "Компоненты: embedding-модель, векторная БД, LLM, фреймворк",
]))
story.append(PageBreak())

# ── Глава 4 ──────────────────────────────────────────────────────────
story.append(chapter_header("4", "ИИ-агенты: автономные действия",
    "Когда ИИ не только отвечает, но и действует",
    level_color=LEVEL_ADVANCED))

story.append(Paragraph(
    "ИИ-агент — это система, в которой языковая модель не просто "
    "отвечает на вопросы, а планирует шаги, вызывает инструменты, "
    "анализирует результаты и принимает решения.", S["Body"]))

story.append(Paragraph("Архитектура агента", S["H2"]))
story.append(code_block(
    "Цель пользователя\n"
    "    ↓\n"
    "LLM планирует шаги (Planner)\n"
    "    ↓\n"
    "┌──→ Выбрать инструмент\n"
    "│       ↓\n"
    "│   Вызвать инструмент (search, code, API, DB)\n"
    "│       ↓\n"
    "│   Получить результат\n"
    "│       ↓\n"
    "│   LLM анализирует: цель достигнута?\n"
    "│       ↓\n"
    "└──  Нет → следующий шаг\n"
    "        Да → финальный ответ"))

story.append(Paragraph("Типы инструментов (tools)", S["H2"]))
story.append(bullet_list([
    "Поиск в интернете (web search, API новостей)",
    "Выполнение кода (Python sandbox, REPL)",
    "Запросы к базе данных (SQL, API)",
    "Чтение/запись файлов",
    "Отправка сообщений (email, Slack, Telegram)",
    "Вызов внешних API (CRM, платёжные системы, аналитика)",
    "Использование других ИИ-моделей (генерация изображений, транскрипция)",
]))

story.append(Paragraph("Фреймворки для агентов", S["H2"]))
story.append(two_col_table([
    ["Фреймворк", "Особенность"],
    ["LangChain Agents", "Гибкий, множество готовых инструментов"],
    ["LangGraph", "Графы состояний для сложных агентов"],
    ["CrewAI", "Мульти-агентные системы с ролями"],
    ["AutoGen (Microsoft)", "Многоагентные диалоги"],
    ["OpenAI Assistants API", "Готовое API от OpenAI с инструментами"],
], col_widths=[48 * mm, 112 * mm]))

story.append(callout(
    "Безопасность агентов",
    "Агенты с доступом к реальным инструментам (код, БД, email) — "
    "это реальная власть. Обязательно: ограничение прав, подтверждение "
    "критичных действий человеком (human-in-the-loop), логирование, "
    "пределы бюджета и времени.",
    bg_color=__import__("book_engine").DANGER_BG, icon="🛡️"))

story.append(key_takeaways([
    "Агент = LLM + инструменты + цикл «план → действие → анализ»",
    "Инструменты: поиск, код, БД, API, коммуникации",
    "Безопасность: ограничение прав, human-in-the-loop, логи",
]))
story.append(PageBreak())

# ── Глава 5 ──────────────────────────────────────────────────────────
story.append(chapter_header("5", "Автоматизация рабочих процессов",
    "Где ИИ экономит время каждый день",
    level_color=LEVEL_BEGINNER))

story.append(Paragraph(
    "ИИ лучше всего работает там, где есть повторяющиеся задачи с "
    "текстом, данными или решениями. Вот конкретные сценарии.", S["Body"]))

scenarios = [
    ("Обработка почты",
     "Сортировка входящих по категориям, черновики ответов, извлечение "
     "ключевых действий из писем."),
    ("Суммаризация документов",
     "Длинные отчёты, договоры, совещания → краткое резюме с ключевыми "
     "пунктами и решениями."),
    ("Создание контента",
     "Посты для соцсетей, описания товаров, email-рассылки, статьи — "
     "черновик за минуты, правка за часы."),
    ("Перевод и локализация",
     "Не просто перевод, а адаптация под культуру, тон и аудиторию "
     "целевого рынка."),
    ("Анализ отзывов",
     "Автоматическая классификация по темам, тональности, выявление "
     "повторяющихся проблем."),
    ("Подготовка данных",
     "Очистка, форматирование, категоризация неструктурированных данных "
     "в таблицы и JSON."),
    ("Код-ревью",
     "Автоматическая проверка PR: баги, стиль, безопасность, "
     "предложения улучшений."),
]

for title, desc in scenarios:
    story.append(Paragraph(f"Сценарий: {title}", S["H3"]))
    story.append(Paragraph(desc, S["Body"]))
    story.append(Spacer(1, 1 * mm))

story.append(callout(
    "Принцип внедрения",
    "Начните с одной повторяющейся задачи. Измерьте время «до» и «после». "
    "Если экономия значимая — масштабируйте. Не пытайтесь автоматизировать "
    "всё сразу.",
    bg_color=__import__("book_engine").TIP_BG, icon="🚀"))

story.append(key_takeaways([
    "ИИ лучше всего для повторяющихся текстовых задач",
    "Начните с одной задачи и измерьте эффект",
    "Суммаризация, контент, анализ, перевод — топ-сценарии",
]))
story.append(PageBreak())

# ── Глава 6 ──────────────────────────────────────────────────────────
story.append(chapter_header("6", "ИИ для контента: текст, изображения, видео",
    "Что умеют генеративные модели",
    level_color=LEVEL_BEGINNER))

story.append(Paragraph("Текст", S["H2"]))
story.append(two_col_table([
    ["Задача", "Инструмент", "Результат"],
    ["Статьи, посты", "ChatGPT, Claude, Jasper", "Черновик за минуты"],
    ["Рекламные тексты", "Copy.ai, Writesonic", "Заголовки, CTA, лендинги"],
    ["SEO-контент", "Surfer SEO + AI", "Оптимизированные статьи"],
    ["Тех. документация", "Claude, GPT-4 + RAG", "Документация по коду/API"],
], col_widths=[40 * mm, 56 * mm, 64 * mm]))

story.append(Paragraph("Изображения", S["H2"]))
story.append(two_col_table([
    ["Инструмент", "Сильная сторона"],
    ["Midjourney", "Художественность, эстетика, стили"],
    ["DALL-E 3", "Точность по промпту, интеграция с ChatGPT"],
    ["Stable Diffusion", "Open-source, локальный запуск, контроль"],
    ["Adobe Firefly", "Коммерческая безопасность, интеграция с Adobe"],
], col_widths=[48 * mm, 112 * mm]))

story.append(Paragraph("Промпт для изображения", S["H3"]))
story.append(code_block(
    "Midjourney:\n"
    "/imagine prompt: editorial photography, modern minimalist office,\n"
    "soft natural light, shallow depth of field, 35mm, color grading\n"
    "teal and orange, high detail, photorealistic --ar 16:9 --v 6"))

story.append(Paragraph("Видео и аудио", S["H2"]))
story.append(bullet_list([
    "Sora / Runway — генерация видео по описанию, до 60 секунд",
    "Synthesia — видео с ИИ-аватаром (презентации, обучение)",
    "ElevenLabs — реалистичная озвучка текста, клонирование голоса",
    "Suno / Udio — генерация музыки с вокалом по описанию",
    "Whisper — транскрипция речи в текст с высокой точностью",
]))

story.append(callout(
    "Авторское право",
    "Контент, созданный ИИ, может иметь ограничения по авторскому праву "
    "в разных юрисдикциях. Проверяйте условия использования платформы "
    "и не используйте чужие бренды/стили художников без разрешения.",
    bg_color=__import__("book_engine").WARN_BG, icon="⚖️"))

story.append(key_takeaways([
    "Текст: ChatGPT, Claude для черновиков; специализированные — для маркетинга",
    "Изображения: Midjourney (арт), DALL-E (точность), SD (контроль)",
    "Видео/аудио: Sora, ElevenLabs, Suno, Whisper",
    "Проверяйте авторские права и условия использования",
]))
story.append(PageBreak())

# ── Глава 7 ──────────────────────────────────────────────────────────
story.append(chapter_header("7", "ИИ в разработке ПО",
    "Copilot, Cursor, ИИ-ассистенты в IDE",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "ИИ изменил процесс написания кода. Автодополнение, генерация "
    "функций, рефакторинг, тесты, документация — всё это ускоряется "
    "в разы.", S["Body"]))

story.append(two_col_table([
    ["Инструмент", "Что делает"],
    ["GitHub Copilot", "Автодополнение кода, генерация функций, коммит-месседжи"],
    ["Cursor", "IDE с ИИ: чат с кодовой базой, мультифайловое редактирование"],
    ["Claude / GPT-4", "Сложные задачи: архитектура, отладка, объяснение кода"],
    ["Codeium / Tabnine", "Бесплатные альтернативы автодополнения"],
    ["v0 / Bolt", "Генерация UI-компонентов и целых приложений по описанию"],
], col_widths=[48 * mm, 112 * mm]))

story.append(Paragraph("Что ИИ делает хорошо в коде", S["H2"]))
story.append(bullet_list([
    "Автодополнение — продолжает код, который вы начали писать",
    "Генерация boilerplate — скелет функции, класса, API-эндпоинта",
    "Тесты — генерация юнит-тестов по реализации",
    "Документация — docstrings, README, комментарии",
    "Рефакторинг — переименование, упрощение, разбиение функций",
    "Отладка — анализ ошибки, предложения исправления",
    "Перевод между языками — Python → Go, JavaScript → TypeScript",
]))

story.append(callout(
    "Где ИИ ошибается в коде",
    "Сложная бизнес-логика, нюансы архитектуры, устаревшие API, "
    "баги в зависимостях. ИИ может предложить код, который выглядит "
    "правильно, но не работает. Всегда проверяйте и тестируйте.",
    bg_color=__import__("book_engine").WARN_BG, icon="⚠️"))

story.append(key_takeaways([
    "Copilot/Cursor ускоряют рутину: boilerplate, тесты, документация",
    "ИИ хорошо генерирует код по описанию, но сложную логику — проверяйте",
    "Используйте ИИ как ассистента, а не замену понимания",
]))
story.append(PageBreak())

# ── Глава 8 ──────────────────────────────────────────────────────────
story.append(chapter_header("8", "ИИ в бизнесе и аналитике",
    "Где ИИ создаёт реальную ценность",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "В бизнесе ИИ применяется не для «инноваций ради инноваций», а для "
    "конкретных задач: снижение затрат, рост выручки, ускорение процессов.",
    S["Body"]))

story.append(two_col_table([
    ["Область", "Применение ИИ", "Эффект"],
    ["Поддержка клиентов", "Чат-боты + RAG по базе знаний", "Снижение нагрузки на 40-60%"],
    ["Продажи", "Оценка лидов, персонализация предложений", "Рост конверсии 15-30%"],
    ["Маркетинг", "Сегментация, A/B-тесты, генерация контента", "Экономия времени на создание кампаний"],
    ["Аналитика", "Анализ отзывов, прогнозы спроса, аномалии", "Быстрее insights, меньше ручной работы"],
    ["HR", "Сортировка резюме, онбординг, обучение", "Скорость найма, персонализация обучения"],
    ["Финансы", "Обнаружение мошенничества, скоринг, отчёты", "Снижение потерь, автоматизация отчётности"],
    ["Логистика", "Оптимизация маршрутов, прогноз запасов", "Снижение затрат на транспортировку"],
], col_widths=[30 * mm, 66 * mm, 64 * mm]))

story.append(Paragraph("Аналитика данных с ИИ", S["H2"]))
story.append(Paragraph(
    "Современные инструменты (ChatGPT Advanced Data Analysis, Julius AI, "
    "Hex Magic) позволяют анализировать данные без кода: загрузить CSV, "
    "задать вопрос на естественном языке, получить график и выводы.",
    S["Body"]))

story.append(code_block(
    "Пример запроса к данным:\n"
    "\n"
    '"Проанализируй продажи за последний квартал. Найди топ-5 продуктов '
    'по выручке, покажи динамику по неделям и выдели аномалии."'))

story.append(key_takeaways([
    "ИИ в бизнесе = снижение затрат + рост выручки",
    "Топ-области: поддержка, продажи, маркетинг, аналитика",
    "Data analysis без кода — реальность с современными инструментами",
]))
story.append(PageBreak())

# ── Глава 9 ──────────────────────────────────────────────────────────
story.append(chapter_header("9", "Безопасная интеграция: что проверять",
    "Чек-лист для внедрения ИИ в продакшен",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "ИИ в продакшене отличается от демо. Вот что нужно проверить перед "
    "запуском и контролировать после.", S["Body"]))

story.append(Paragraph("До запуска", S["H2"]))
story.append(numbered_list([
    "Валидация входа: проверка размера, формата, содержания пользовательского ввода",
    "Ограничение rate limit: защита от перебора и злоупотреблений",
    "Бюджет на API: оценка стоимости и установка лимитов (дневных, месячных)",
    "Fallback: что происходит, если API недоступен или отвечает с ошибкой",
    "Приватность данных: не отправляются ли чувствительные данные в облачный API",
    "Тестирование на галлюцинации: проверка типичных запросов и edge cases",
    "Инструкции безопасности в system prompt: что модель не должна делать",
]))

story.append(Paragraph("В продакшене", S["H2"]))
story.append(numbered_list([
    "Логирование всех запросов и ответов (без чувствительных данных)",
    "Мониторинг стоимости, задержки, ошибок",
    "Оповещения при всплеске ошибок или стоимости",
    "Регулярная проверка качества ответов (выборка + оценка)",
    "Обновление моделей: тестировать перед переключением",
    "Сбор фидбека от пользователей (thumbs up/down, комментарии)",
]))

story.append(callout(
    "Промпт-инъекции — главная угроза",
    "Злоумышленник может встроить инструкции в пользовательский ввод, "
    "чтобы заставить модель проигнорировать системные правила. "
    "Никогда не вставляйте пользовательский текст в system prompt без "
    "санитизации. Разделяйте инструкции и данные.",
    bg_color=__import__("book_engine").DANGER_BG, icon="🚨"))

story.append(key_takeaways([
    "Валидация входа, rate limit, бюджет, fallback — обязательны",
    "Логирование и мониторинг — в продакшене",
    "Промпт-инъекции — главная угроза, разделяйте инструкции и данные",
]))
story.append(PageBreak())

# ── Глава 10: Практикум ──────────────────────────────────────────────
story.append(chapter_header("10", "Практикум: строим RAG-систему",
    "Минимальный RAG на Python за 50 строк",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "Минимальная RAG-система: читаем документы, создаём embeddings, "
    "ищем по запросу, генерируем ответ.", S["Body"]))

story.append(code_block(
    "import openai\n"
    "import numpy as np\n"
    "\n"
    "client = openai.OpenAI(api_key=\"sk-...\")\n"
    "\n"
    "# 1. Документы\n"
    "docs = [\n"
    "    \"GPT-4 выпущен в марте 2023 года, имеет 128K контекст.\",\n"
    "    \"Claude 3 Opus от Anthropic выпущен в марте 2024.\",\n"
    "    \"LLaMA 2 — open-source модель от Meta, 70B параметров.\",\n"
    "]\n"
    "\n"
    "# 2. Embeddings\n"
    "def embed(text):\n"
    "    r = client.embeddings.create(\n"
    "        model=\"text-embedding-3-small\", input=text)\n"
    "    return np.array(r.data[0].embedding)\n"
    "\n"
    "doc_vectors = [embed(d) for d in docs]\n"
    "\n"
    "# 3. Поиск\n"
    "def search(query, top_k=2):\n"
    "    q_vec = embed(query)\n"
    "    scores = [np.dot(q_vec, dv) for dv in doc_vectors]\n"
    "    idx = np.argsort(scores)[-top_k:][::-1]\n"
    "    return [docs[i] for i in idx]\n"
    "\n"
    "# 4. Ответ\n"
    "def answer(query):\n"
    "    context = \"\\n\".join(search(query))\n"
    "    r = client.chat.completions.create(\n"
    "        model=\"gpt-4o\",\n"
    "        messages=[\n"
    "            {\"role\": \"system\",\n"
    "             \"content\": f\"Ответь по контексту. Если нет данных — скажи.\\n\\n{context}\"},\n"
    "            {\"role\": \"user\", \"content\": query},\n"
    "        ])\n"
    "    return r.choices[0].message.content\n"
    "\n"
    "print(answer(\"Какая модель open-source?\"))\n"
    "# → \"LLaMA 2 — open-source модель от Meta, 70B параметров.\""))

story.append(Paragraph("Что улучшить для продакшена", S["H2"]))
story.append(bullet_list([
    "Векторная БД вместо списка (Pinecone, Qdrant, pgvector)",
    "Разбиение документов на chunks (не целые документы)",
    "Гибридный поиск: векторный + ключевое слово (BM25)",
    "Переранжирование результатов (cross-encoder)",
    "Кэширование embeddings и ответов",
    "Цитирование источников в ответе",
    "Оценка качества: RAGAS или ручная выборка",
]))

story.append(Spacer(1, 10 * mm))
story.append(HRFlowable(width="100%", thickness=0.8, color=ACCENT, spaceAfter=6))
story.append(Paragraph(
    "Конец Книги 4. Следующая — Книга 5: Этика, безопасность и "
    "ограничения ИИ.", S["Caption"]))

build_book(
    "Kniga-4-Prakticheskoe-Primenenie-II.pdf",
    "Библиотека ИИ",
    "Практическое применение ИИ",
    "K4",
    story,
    "Библиотека ИИ · Книга 4 · Практика",
)
print("Книга 4 построена.")
