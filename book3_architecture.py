# -*- coding: utf-8 -*-
"""Книга 3: Архитектура нейросетей и трансформеров.

Нейрон, обратное распространение, механизм внимания, токенизация,
RLHF, законы масштабирования.
"""
from reportlab.platypus import Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.lib.units import mm
from book_engine import (
    S, build_book, chapter_header, bullet_list, numbered_list,
    callout, key_takeaways, code_block, two_col_table, level_badge,
    LEVEL_INTER, LEVEL_ADVANCED, ACCENT, CODE_LN,
)

story = []

# ── Обложка ──────────────────────────────────────────────────────────
story.append(Spacer(1, 50 * mm))
story.append(Paragraph("Книга 3", S["Cover"]))
story.append(Spacer(1, 4 * mm))
story.append(Paragraph("Архитектура нейросетей и трансформеров", S["BookTitle"]))
story.append(Paragraph(
    "Нейрон, обратное распространение, механизм внимания, токенизация, "
    "RLHF, законы масштабирования", S["BookSubtitle"]))
story.append(Spacer(1, 6 * mm))
story.append(HRFlowable(width="40%", thickness=1.2, color=ACCENT,
                        spaceAfter=6, hAlign="CENTER"))
story.append(level_badge("Средний — Продвинутый", LEVEL_ADVANCED))
story.append(Spacer(1, 60 * mm))
story.append(Paragraph("Библиотека ИИ · Книга 3 из 5", S["Cover"]))
story.append(PageBreak())

# ── Оглавление ───────────────────────────────────────────────────────
story.append(Paragraph("Содержание", S["H1"]))
story.append(HRFlowable(width="100%", thickness=0.5, color=CODE_LN, spaceAfter=8))
toc = [
    "1. Математика одного нейрона",
    "2. Активационные функции",
    "3. Прямой проход (forward pass)",
    "4. Функции потерь",
    "5. Обратное распространение ошибки (backpropagation)",
    "6. Оптимизаторы: SGD, Adam, AdamW",
    "7. Токенизация: BPE, WordPiece, SentencePiece",
    "8. Embeddings: векторы слов и предложений",
    "9. Механизм внимания (Self-Attention)",
    "10. Архитектура трансформера",
    "11. Предобучение: MLM и CLM",
    "12. RLHF и DPO: настройка по человеческим оценкам",
    "13. Законы масштабирования (Scaling Laws)",
    "14. Современные архитектуры: Mixture-of-Experts, Flash Attention",
]
story.append(numbered_list(toc))
story.append(PageBreak())

# ── Глава 1 ──────────────────────────────────────────────────────────
story.append(chapter_header("1", "Математика одного нейрона",
    "Линейная комбинация + нелинейность",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "Нейрон — минимальный вычислительный элемент нейросети. "
    "Математически он выполняет две операции: взвешенную сумму входов "
    "и применение нелинейной функции активации.", S["Body"]))

story.append(Paragraph("Формула", S["H2"]))
story.append(code_block(
    "z = w₁x₁ + w₂x₂ + ... + wₙxₙ + b\n"
    "a = f(z)\n"
    "\n"
    "где:\n"
    "  xᵢ — входные значения (признаки)\n"
    "  wᵢ — веса (learnable parameters)\n"
    "  b  — смещение (bias)\n"
    "  z  — линейная комбинация (pre-activation)\n"
    "  f  — функция активации (нелинейная)\n"
    "  a  — выход нейрона (activation)"))

story.append(Paragraph("Векторная форма", S["H2"]))
story.append(code_block(
    "z = W·x + b\n"
    "a = f(z)\n"
    "\n"
    "W — матрица весов [out_dim × in_dim]\n"
    "x — вектор входов [in_dim]\n"
    "b — вектор смещений [out_dim]"))

story.append(callout(
    "Почему важна нелинейность",
    "Без функции активации (f) нейрон — это просто линейная регрессия. "
    "Стек линейных слоёв всё равно даёт линейное преобразование. "
    "Нелинейность позволяет сети аппроксимировать произвольные функции "
    "(теорема универсальной аппроксимации).",
    bg_color=__import__("book_engine").TIP_BG, icon="🧠"))

story.append(key_takeaways([
    "Нейрон = взвешенная сумма + нелинейная активация",
    "Векторная форма: a = f(W·x + b)",
    "Нелинейность критически важна — без неё сеть = линейная модель",
]))
story.append(PageBreak())

# ── Глава 2 ──────────────────────────────────────────────────────────
story.append(chapter_header("2", "Активационные функции",
    "ReLU, Sigmoid, Tanh, GELU, SwiGLU",
    level_color=LEVEL_INTER))

story.append(two_col_table([
    ["Функция", "Формула", "Где используется"],
    ["ReLU", "max(0, z)", "Скрытые слои в CNN, базовый выбор"],
    ["Sigmoid", "1 / (1 + e⁻ᶻ)", "Бинарная классификация, gated RNN"],
    ["Tanh", "(eᶻ - e⁻ᶻ) / (eᶻ + e⁻ᶻ)", "RNN, когда нужно [-1, 1]"],
    ["GELU", "z · Φ(z)", "Трансформеры (BERT, GPT)"],
    ["SwiGLU", "Swish(z) · (zW₂)", "Современные LLM (LLaMA, PaLM)"],
    ["Softmax", "eᶻᵢ / Σeᶻⱼ", "Выходной слой классификации"],
], col_widths=[30 * mm, 48 * mm, 82 * mm]))

story.append(Paragraph("ReLU (Rectified Linear Unit)", S["H2"]))
story.append(code_block(
    "f(z) = max(0, z)\n"
    "\n"
    "  z > 0  → f(z) = z   (пропускает сигнал)\n"
    "  z ≤ 0  → f(z) = 0   (блокирует сигнал)\n"
    "\n"
    "Плюсы: простая, быстрая, нет проблемы затухающего градиента\n"
    "       для положительных значений\n"
    "Минусы: «мертвые нейроны» — при z < 0 градиент = 0"))

story.append(Paragraph("GELU (Gaussian Error Linear Unit)", S["H2"]))
story.append(Paragraph(
    "Используется в трансформерах. Гладкий аналог ReLU, который "
    "даёт небольшое отрицательное значение для z < 0, что уменьшает "
    "проблему мёртвых нейронов.", S["Body"]))
story.append(code_block(
    "GELU(z) ≈ 0.5z · (1 + tanh(√(2/π) · (z + 0.044715z³)))"))

story.append(key_takeaways([
    "ReLU — базовый выбор для скрытых слоёв",
    "GELU — стандарт для трансформеров",
    "SwiGLU — современный вариант для LLM",
    "Softmax — для выходного слоя классификации",
]))
story.append(PageBreak())

# ── Глава 3 ──────────────────────────────────────────────────────────
story.append(chapter_header("3", "Прямой проход (forward pass)",
    "Как данные проходят через сеть",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "Прямой проход — это вычисление выхода сети по входным данным. "
    "Данные проходят последовательно через все слои.", S["Body"]))

story.append(code_block(
    "Слой 0 (вход):  x = [x₁, x₂, x₃]\n"
    "\n"
    "Слой 1 (скрытый):  z₁ = W₁·x + b₁\n"
    "                   a₁ = ReLU(z₁)\n"
    "\n"
    "Слой 2 (скрытый):  z₂ = W₂·a₁ + b₂\n"
    "                   a₂ = ReLU(z₂)\n"
    "\n"
    "Слой 3 (выход):    z₃ = W₃·a₂ + b₃\n"
    "                   ŷ  = softmax(z₃)   # вероятности классов"))

story.append(Paragraph("Размерности", S["H2"]))
story.append(code_block(
    "Пример: вход 3 признака, 2 скрытых слоя по 64 нейрона, 10 классов\n"
    "\n"
    "  W₁: [64 × 3]    b₁: [64]\n"
    "  W₂: [64 × 64]   b₂: [64]\n"
    "  W₃: [10 × 64]   b₃: [10]\n"
    "\n"
    "  Всего параметров: 64×3 + 64 + 64×64 + 64 + 10×64 + 10 = 4,522"))

story.append(key_takeaways([
    "Forward pass — вычисление выхода сети по входу",
    "Каждый слой: z = W·a_prev + b, затем a = f(z)",
    "Количество параметров = сумма размерностей всех весов и смещений",
]))
story.append(PageBreak())

# ── Глава 4 ──────────────────────────────────────────────────────────
story.append(chapter_header("4", "Функции потерь",
    "Как измеряется ошибка",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "Функция потерь (loss function) измеряет, насколько предсказание "
    "модели отличается от правильного ответа. Цель обучения — минимизировать "
    "среднее значение потерь по всем примерам.", S["Body"]))

story.append(two_col_table([
    ["Функция", "Формула", "Задача"],
    ["MSE", "Σ(ŷᵢ - yᵢ)² / N", "Регрессия"],
    ["Cross-Entropy", "-Σ yᵢ log(ŷᵢ)", "Классификация"],
    ["Binary CE", "-[y·log(ŷ) + (1-y)·log(1-ŷ)]", "Бинарная классификация"],
    ["KL Divergence", "Σ yᵢ log(yᵢ / ŷᵢ)", "Распределения вероятностей"],
    ["Huber Loss", "гибрид MSE + MAE", "Регрессия с выбросами"],
], col_widths=[34 * mm, 64 * mm, 62 * mm]))

story.append(Paragraph("Cross-Entropy для классификации", S["H2"]))
story.append(code_block(
    "L = -Σᵢ yᵢ · log(ŷᵢ)\n"
    "\n"
    "где:\n"
    "  yᵢ — истинная метка (one-hot): [0, 0, 1, 0, ...]\n"
    "  ŷᵢ — предсказанная вероятность класса i\n"
    "\n"
    "Если модель уверена в правильном классе (ŷ → 1) → loss → 0\n"
    "Если модель уверена в неправильном → loss → ∞"))

story.append(Paragraph("Perplexity (для языковых моделей)", S["H2"]))
story.append(Paragraph(
    "Perplexity = exp(cross-entropy). Мера того, насколько модель "
    "«удивлена» правильным ответом. Чем ниже — тем лучше. "
    "PPL = 1 — идеальная модель, PPL = |словарь| — случайная.",
    S["Body"]))

story.append(key_takeaways([
    "MSE — для регрессии, Cross-Entropy — для классификации",
    "Cross-Entropy сильно штрафует уверенность в неправильном ответе",
    "Perplexity = exp(loss) — метрика качества языковых моделей",
]))
story.append(PageBreak())

# ── Глава 5 ──────────────────────────────────────────────────────────
story.append(chapter_header("5", "Обратное распространение (backpropagation)",
    "Как градиенты доходят до каждого веса",
    level_color=LEVEL_ADVANCED))

story.append(Paragraph(
    "Backpropagation — алгоритм вычисления градиентов функции потерь "
    "по каждому параметру сети. Основан на правиле дифференцирования "
    "сложной функции (chain rule).", S["Body"]))

story.append(Paragraph("Chain Rule — основа", S["H2"]))
story.append(code_block(
    "Если y = f(g(x)), то dy/dx = f'(g(x)) · g'(x)\n"
    "\n"
    "Для нейросети:\n"
    "  ∂L/∂W₃ = ∂L/∂ŷ · ∂ŷ/∂z₃ · ∂z₃/∂W₃\n"
    "\n"
    "  ∂L/∂W₂ = ∂L/∂z₃ · ∂z₃/∂a₂ · ∂a₂/∂z₂ · ∂z₂/∂W₂\n"
    "\n"
    "  ∂L/∂W₁ = ∂L/∂z₂ · ∂z₂/∂a₁ · ∂a₁/∂z₁ · ∂z₁/∂W₁"))

story.append(Paragraph("Алгоритм", S["H2"]))
story.append(numbered_list([
    "Forward pass: вычислить все z и a для каждого слоя",
    "Вычислить loss L по выходу сети",
    "Вычислить градиент loss по выходу: ∂L/∂ŷ",
    "Двигаясь от последнего слоя к первому, вычислять градиенты "
    "по каждому слою через chain rule",
    "Для каждого веса: ∂L/∂Wᵢ = градиент × выход предыдущего слоя",
    "Обновить веса: W = W - η · ∂L/∂W (где η — скорость обучения)",
]))

story.append(callout(
    "Затухающий градиент",
    "В глубоких сетях градиенты могут становиться очень маленькими при "
    "прохождении через слои (особенно с sigmoid/tanh). До первых слоёв "
    "градиент почти не доходит — они не обучаются. Решения: ReLU, "
    "residual connections, batch normalization, gradient clipping.",
    bg_color=__import__("book_engine").WARN_BG, icon="⚠️"))

story.append(key_takeaways([
    "Backprop = chain rule для вычисления ∂L/∂W для каждого слоя",
    "Градиенты идут от выхода к входу (обратный проход)",
    "Веса обновляются: W = W - η · ∂L/∂W",
    "Затухающий градиент — проблема глубоких сетей, решается ReLU и residual",
]))
story.append(PageBreak())

# ── Глава 6 ──────────────────────────────────────────────────────────
story.append(chapter_header("6", "Оптимизаторы: SGD, Adam, AdamW",
    "Как обновляются веса",
    level_color=LEVEL_INTER))

story.append(two_col_table([
    ["Оптимизатор", "Идея", "Когда использовать"],
    ["SGD", "W = W - η · ∇L", "Простой, с momentum — эффективен для больших моделей"],
    ["SGD+Momentum", "v = βv + ∇L; W = W - ηv", "Ускоряет движение в правильном направлении"],
    ["RMSprop", "Адаптивный шаг для каждого параметра", "RNN, нестационарные цели"],
    ["Adam", "Momentum + RMSprop вместе", "Универсальный, большинство задач"],
    ["AdamW", "Adam + decoupled weight decay", "Трансформеры, LLM (стандарт)"],
], col_widths=[34 * mm, 62 * mm, 64 * mm]))

story.append(Paragraph("Adam — формула", S["H2"]))
story.append(code_block(
    "m = β₁·m + (1-β₁)·∇L          # момент (экспоненциальное среднее градиента)\n"
    "v = β₂·v + (1-β₂)·(∇L)²       # экспоненциальное среднее квадрата градиента\n"
    "m̂ = m / (1-β₁ᵗ)               # коррекция смещения\n"
    "v̂ = v / (1-β₂ᵗ)\n"
    "W = W - η · m̂ / (√v̂ + ε)\n"
    "\n"
    "Типичные значения: β₁=0.9, β₂=0.999, ε=1e-8, η=1e-3..1e-5"))

story.append(Paragraph("AdamW — почему не просто Adam", S["H2"]))
story.append(Paragraph(
    "В классическом Adam weight decay реализован через L2-регуляризацию "
    "в градиенте. Это искажает адаптивные шаги. AdamW разделяет их: "
    "адаптивный шаг от Adam + независимый weight decay. "
    "Это даёт лучшую обобщающую способность для трансформеров.", S["Body"]))

story.append(key_takeaways([
    "SGD — простой, Adam — универсальный, AdamW — стандарт для LLM",
    "Adam: momentum + адаптивный шаг на параметр",
    "AdamW: разделяет weight decay и адаптивный шаг",
]))
story.append(PageBreak())

# ── Глава 7 ──────────────────────────────────────────────────────────
story.append(chapter_header("7", "Токенизация: BPE, WordPiece, SentencePiece",
    "Как текст превращается в токены",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "Токенизация — процесс разбиения текста на токены. Это первый шаг "
    "перед подачей текста в модель. От качества токенизации зависит "
    "эффективность и многоязычность модели.", S["Body"]))

story.append(Paragraph("BPE (Byte-Pair Encoding)", S["H2"]))
story.append(Paragraph(
    "Самый распространённый метод. Начинает с отдельных символов, "
    "затем итеративно объединяет самые частые пары в новые токены.",
    S["Body"]))
story.append(code_block(
    "Шаг 0: l o w </w>          (символы)\n"
    "Шаг 1: lo w </w>           (l+o → lo, часто встречается)\n"
    "Шаг 2: low </w>            (lo+w → low)\n"
    "Шаг 3: low</w>             (low+</w> → слово)\n"
    "\n"
    "В итоге: «lower» → [low, er]  (2 токена вместо 5 символов)"))

story.append(Paragraph("WordPiece", S["H2"]))
story.append(Paragraph(
    "Похож на BPE, но объединяет пары, максимизирующие правдоподобие "
    "обучающего корпуса. Используется в BERT. Токены-продолжения "
    "начинаются с ## (##ing, ##ed).", S["Body"]))

story.append(Paragraph("SentencePiece", S["H2"]))
story.append(Paragraph(
    "Работает на уровне байтов, не зависит от пробелов. "
    "Поддерживает любые языки, включая те, где нет пробелов между "
    "словами (китайский, японский, тайский). Используется в LLaMA, T5.",
    S["Body"]))

story.append(two_col_table([
    ["Метод", "Модели", "Особенность"],
    ["BPE", "GPT-2, GPT-3, GPT-4", "Частотное объединение пар"],
    ["WordPiece", "BERT, DistilBERT", "Правдоподобие, ##-префикс"],
    ["SentencePiece", "LLaMA, T5, ALBERT", "Байтовый уровень, язык-агностик"],
], col_widths=[36 * mm, 52 * mm, 72 * mm]))

story.append(key_takeaways([
    "BPE — стандарт для GPT-семейства",
    "WordPiece — для BERT, использует ##-префиксы",
    "SentencePiece — для многоязычных моделей, работает на уровне байтов",
]))
story.append(PageBreak())

# ── Глава 8 ──────────────────────────────────────────────────────────
story.append(chapter_header("8", "Embeddings: векторы слов и предложений",
    "Как слова становятся числами",
    level_color=LEVEL_INTER))

story.append(Paragraph(
    "Embedding — это отображение дискретных токенов в непрерывные "
    "векторы. Вектор обучается так, что похожие по смыслу слова "
    "оказываются близко друг к другу в векторном пространстве.",
    S["Body"]))

story.append(Paragraph("Embedding-слой", S["H2"]))
story.append(code_block(
    "Словарь: V = 50,000 токенов\n"
    "Размерность: d = 768\n"
    "\n"
    "Embedding-матрица: E [V × d] = [50000 × 768]\n"
    "\n"
    "Токен с ID=42 → E[42] → вектор [768 чисел]\n"
    "\n"
    "Эта матрица — обучаемые параметры модели."))

story.append(Paragraph("Свойства embedding-пространства", S["H2"]))
story.append(code_block(
    "король - мужчина + женщина ≈ королева\n"
    "Париж - Франция + Германия ≈ Берлин\n"
    "\n"
    'cos(вектор(«кошка»), вектор(«собака»)) > cos(вектор(«кошка»), вектор(«стол»))\n'
    "\n"
    "где cos(a, b) = (a·b) / (|a|·|b|) — косинусное сходство"))

story.append(Paragraph("Positional Encoding", S["H2"]))
story.append(Paragraph(
    "Трансформер обрабатывает все токены одновременно, поэтому "
    "ему нужно явно указать порядок. Positional encoding добавляет "
    "информацию о позиции к embedding-вектору.", S["Body"]))

story.append(code_block(
    "Синусоидальный (оригинальный трансформер):\n"
    "PE(pos, 2i)   = sin(pos / 10000^(2i/d))\n"
    "PE(pos, 2i+1) = cos(pos / 10000^(2i/d))\n"
    "\n"
    "RoPE (Rotary Position Embedding) — современный вариант:\n"
    "поворачивает embedding-векторы в зависимости от позиции.\n"
    "Используется в LLaMA, GPT-NeoX, PaLM."))

story.append(key_takeaways([
    "Embedding = таблица V×d, обучается вместе с моделью",
    "Похожие слова → близкие векторы (cosine similarity)",
    "Positional encoding добавляет информацию о порядке токенов",
    "RoPE — современный метод для позиций в LLM",
]))
story.append(PageBreak())

# ── Глава 9 ──────────────────────────────────────────────────────────
story.append(chapter_header("9", "Механизм внимания (Self-Attention)",
    "Сердце трансформера",
    level_color=LEVEL_ADVANCED))

story.append(Paragraph(
    "Attention — механизм, позволяющий модели «смотреть» на все "
    "токены входа и определять, какие из них важны для каждого "
    "выходного токена.", S["Body"]))

story.append(Paragraph("Scaled Dot-Product Attention", S["H2"]))
story.append(code_block(
    "Attention(Q, K, V) = softmax(Q·Kᵀ / √dₖ) · V\n"
    "\n"
    "где:\n"
    "  Q (Query)  = X · Wq   — «что я ищу»\n"
    "  K (Key)    = X · Wk   — «что у меня есть»\n"
    "  V (Value)  = X · Wv   — «содержание»\n"
    "  dₖ — размерность ключа (деление на √dₖ стабилизирует градиент)\n"
    "\n"
    "Q·Kᵀ — матрица «скоролов» [seq_len × seq_len]\n"
    "softmax — превращает скоры в вероятности (сумма = 1)\n"
    "× V — взвешенная сумма значений"))

story.append(Paragraph("Multi-Head Attention", S["H2"]))
story.append(Paragraph(
    "Вместо одного attention модель использует несколько «голов» (heads), "
    "каждая смотрит на разные аспекты отношений между токенами.", S["Body"]))
story.append(code_block(
    "MultiHead(Q,K,V) = Concat(head₁, head₂, ..., headₕ) · W_O\n"
    "\n"
    "headᵢ = Attention(Q·Wqᵢ, K·Wkᵢ, V·Wvᵢ)\n"
    "\n"
    "Пример: d_model=768, h=12 голов → каждая голова d=768/12=64"))

story.append(Paragraph("Causal (Masked) Attention", S["H2"]))
story.append(Paragraph(
    "В языковых моделях каждый токен может «видеть» только предыдущие, "
    "но не будущие. Это достигается маскированием: будущим позициям "
    "присваивается -∞ перед softmax, что даёт вес 0.", S["Body"]))

story.append(code_block(
    "Mask (для seq_len=4):\n"
    "[  0,  -∞, -∞, -∞ ]\n"
    "[  0,   0, -∞, -∞ ]\n"
    "[  0,   0,  0, -∞ ]\n"
    "[  0,   0,  0,  0  ]\n"
    "\n"
    "После softmax: нижний треугольник, верхний = 0"))

story.append(key_takeaways([
    "Attention(Q,K,V) = softmax(Q·Kᵀ/√dₖ)·V",
    "Multi-head: несколько голов параллельно, потом concat",
    "Causal mask: каждый токен видит только прошлые — для LLM",
]))
story.append(PageBreak())

# ── Глава 10 ─────────────────────────────────────────────────────────
story.append(chapter_header("10", "Архитектура трансформера",
    "Сборка блоков в полную модель",
    level_color=LEVEL_ADVANCED))

story.append(Paragraph(
    "Трансформер состоит из повторяющихся блоков. "
    "Каждый блок: Multi-Head Attention + Feed-Forward Network, "
    "с residual connections и layer normalization.", S["Body"]))

story.append(Paragraph("Блок трансформера (Decoder-only, как GPT)", S["H2"]))
story.append(code_block(
    "Вход: x [batch, seq_len, d_model]\n"
    "\n"
    "  ┌──────────────────────────────────┐\n"
    "  │ 1. Causal Multi-Head Attention   │\n"
    "  │    x' = MHA(x)                   │\n"
    "  │    x = x + x'        (residual)  │\n"
    "  │    x = LayerNorm(x)              │\n"
    "  ├──────────────────────────────────┤\n"
    "  │ 2. Feed-Forward Network           │\n"
    "  │    x' = Linear(ReLU(Linear(x)))  │\n"
    "  │    x = x + x'        (residual)  │\n"
    "  │    x = LayerNorm(x)              │\n"
    "  └──────────────────────────────────┘\n"
    "     ↑ повторить N раз (слоёв)\n"
    "\n"
    "Выход: logits = Linear(x)  [batch, seq_len, vocab_size]"))

story.append(Paragraph("Ключевые гиперпараметры", S["H2"]))
story.append(two_col_table([
    ["Параметр", "GPT-2 small", "GPT-3", "LLaMA-2 70B"],
    ["Слоёв (n_layers)", "12", "96", "80"],
    ["d_model", "768", "12288", "8192"],
    ["Голов (n_heads)", "12", "96", "64"],
    ["Параметров", "124M", "175B", "70B"],
    ["Контекст", "1024", "2048", "4096"],
], col_widths=[44 * mm, 38 * mm, 38 * mm, 40 * mm]))

story.append(Paragraph("Residual Connections — зачем", S["H2"]))
story.append(Paragraph(
    "Residual (x = x + f(x)) позволяет градиенту проходить напрямую "
    "через все слои. Без них глубокие сети (50+ слоёв) не обучаются. "
    "Также позволяет модели «пропускать» преобразование, если оно "
    "не нужно для данного входа.", S["Body"]))

story.append(key_takeaways([
    "Трансформер = стек из N блоков (Attention + FFN + residual + norm)",
    "Residual connections критичны для глубоких сетей",
    "Decoder-only архитектура (GPT) — стандарт для LLM",
]))
story.append(PageBreak())

# ── Глава 11 ─────────────────────────────────────────────────────────
story.append(chapter_header("11", "Предобучение: MLM и CLM",
    "Как модели учатся языку",
    level_color=LEVEL_INTER))

story.append(Paragraph("Masked Language Modeling (MLM)", S["H2"]))
story.append(Paragraph(
    "Используется в BERT. Часть токенов маскируется, модель должна "
    "предсказать их. Модель видит контекст с обеих сторон (двунаправленная).",
    S["Body"]))
story.append(code_block(
    "Вход:  «[MASK] сидел на [MASK]»\n"
    "Цель:  предсказать «Кот» и «ковре»\n"
    "Маскируется ~15% токенов случайно"))

story.append(Paragraph("Causal Language Modeling (CLM)", S["H2"]))
story.append(Paragraph(
    "Используется в GPT. Модель предсказывает следующий токен, "
    "видя только предыдущие (однонаправленная).", S["Body"]))
story.append(code_block(
    "Вход:  «Кот сидел на»\n"
    "Цель:  «ковре»\n"
    "\n"
    "Loss = -log P(ковре | Кот, сидел, на)"))

story.append(two_col_table([
    ["Свойство", "MLM (BERT)", "CLM (GPT)"],
    ["Направление", "Двунаправленная", "Однонаправленная (слева направо)"],
    ["Задача", "Предсказать [MASK]", "Предсказать следующий токен"],
    ["Генерация", "Нет", "Да (авторегрессионная)"],
    ["Лучше для", "Понимание текста, классификация", "Генерация текста, диалоги"],
], col_widths=[34 * mm, 62 * mm, 64 * mm]))

story.append(key_takeaways([
    "MLM (BERT): маскируем токены, предсказываем их, двунаправленная",
    "CLM (GPT): предсказываем следующий токен, однонаправленная",
    "CLM — основа всех генеративных LLM (ChatGPT, Claude, LLaMA)",
]))
story.append(PageBreak())

# ── Глава 12 ─────────────────────────────────────────────────────────
story.append(chapter_header("12", "RLHF и DPO: настройка по оценкам людей",
    "От сырой модели к полезной и безопасной",
    level_color=LEVEL_ADVANCED))

story.append(Paragraph(
    "После предобучения модель умеет генерировать текст, но не всегда "
    "следует инструкциям и может быть небезопасной. RLHF и DPO — "
    "методы дообучения, использующие оценки людей.", S["Body"]))

story.append(Paragraph("RLHF (Reinforcement Learning from Human Feedback)", S["H2"]))
story.append(numbered_list([
    "Собрать человеческие оценки: для одного промпта — несколько ответов "
    "модели, люди ранжируют их от лучшего к худшему",
    "Обучить модель наград (reward model) предсказывать человеческие "
    "предпочтения",
    "Оптимизировать языковую модель с помощью PPO (Proximal Policy "
    "Optimization), максимизируя награду от reward model",
    "Контролировать, что модель не «забыла» язык (KL-дивергенция с "
    "исходной моделью)",
]))

story.append(code_block(
    "Схема RLHF:\n"
    "\n"
    "  Промпт → LLM → 2 ответа → Человек ранжирует\n"
    "                                    ↓\n"
    "                           Reward Model\n"
    "                                    ↓\n"
    "  Промпт → LLM → ответ → Reward Model → награда → PPO → обновление LLM"))

story.append(Paragraph("DPO (Direct Preference Optimization)", S["H2"]))
story.append(Paragraph(
    "Более новый метод (2023). Обходит reward model и PPO — "
    "оптимизирует модель напрямую по парам предпочтений. Проще, "
    "стабильнее и дешевле, чем RLHF. Используется в LLaMA-3, Zephyr.",
    S["Body"]))

story.append(code_block(
    "DPO loss:\n"
    "L = -log σ(β · [log π(y_w|x)/π_ref(y_w|x)\n"
    "               - log π(y_l|x)/π_ref(y_l|x)])\n"
    "\n"
    "где:\n"
    "  y_w — предпочтительный ответ (winner)\n"
    "  y_l — менее предпочтительный (loser)\n"
    "  π — текущая модель, π_ref — исходная\n"
    "  β — параметр регуляризации"))

story.append(key_takeaways([
    "RLHF: reward model + PPO, сложнее но проверенный",
    "DPO: прямая оптимизация по парам, проще и стабильнее",
    "Оба метода делают модель более полезной и безопасной",
]))
story.append(PageBreak())

# ── Глава 13 ─────────────────────────────────────────────────────────
story.append(chapter_header("13", "Законы масштабирования (Scaling Laws)",
    "Как размер модели, данных и вычислений влияют на loss",
    level_color=LEVEL_ADVANCED))

story.append(Paragraph(
    "Исследования OpenAI (2020) и DeepMind (Chinchilla, 2022) показали, "
    "что loss модели предсказуемо уменьшается с ростом параметров, "
    "данных и вычислений — по степенному закону.", S["Body"]))

story.append(Paragraph("Kaplan et al. (OpenAI, 2020)", S["H2"]))
story.append(code_block(
    "L(N) ∝ N^(-α)\n"
    "\n"
    "где:\n"
    "  L — loss (cross-entropy)\n"
    "  N — количество параметров\n"
    "  α ≈ 0.076\n"
    "\n"
    "Вывод: больше параметров → ниже loss, предсказуемо"))

story.append(Paragraph("Chinchilla (DeepMind, 2022)", S["H2"]))
story.append(Paragraph(
    "Показала, что предыдущие модели были «недообучены» — параметров "
    "много, а данных мало. Оптимальное соотношение:", S["Body"]))
story.append(code_block(
    "D_optimal ≈ 20 × N\n"
    "\n"
    "То есть: для модели с 70B параметров нужно ~1.4T токенов данных\n"
    "\n"
    "Пример:\n"
    "  GPT-3: 175B параметров, 300B токенов → недообучена\n"
    "  Chinchilla: 70B параметров, 1.4T токенов → лучше при меньшем размере"))

story.append(callout(
    "Практическое следствие",
    "Удвоение размера модели без удвоения данных — пустая трата. "
    "Бюджет на данные должен расти пропорционально размеру модели. "
    "Это изменило подход к обучению LLM в 2022-2024 годах.",
    bg_color=__import__("book_engine").TIP_BG, icon="📈"))

story.append(key_takeaways([
    "Loss уменьшается по степенному закону с ростом параметров и данных",
    "Chinchilla: оптимально ~20 токенов на параметр",
    "Многие большие модели были недообучены — данных было мало",
]))
story.append(PageBreak())

# ── Глава 14 ─────────────────────────────────────────────────────────
story.append(chapter_header("14", "Современные архитектуры",
    "Mixture-of-Experts, Flash Attention, KV Cache",
    level_color=LEVEL_ADVANCED))

story.append(Paragraph("Mixture-of-Experts (MoE)", S["H2"]))
story.append(Paragraph(
    "Вместо одной большой FFN — несколько «экспертов» (FFN), и маршрутизатор "
    "(router) выбирает 2-4 эксперта для каждого токена. Это позволяет "
    "иметь большую общую ёмкость при той же стоимости инференса.",
    S["Body"]))
story.append(code_block(
    "Пример: Mixtral 8×7B\n"
    "  8 экспертов по 7B параметров\n"
    "  На каждый токен: 2 эксперта активны\n"
    "  Общих параметров: 46.7B\n"
    "  Активных на токен: 12.9B\n"
    "  → качество как у 47B модели, скорость как у 13B"))

story.append(Paragraph("Flash Attention", S["H2"]))
story.append(Paragraph(
    "Optimized алгоритм attention, который минимизирует чтения/записи "
    "в GPU память. Даёт 2-4x ускорение и экономит память, не меняя "
    "математический результат.", S["Body"]))

story.append(Paragraph("KV Cache", S["H2"]))
story.append(Paragraph(
    "При авторегрессионной генерации каждый новый токен пересчитывает "
    "attention со всеми предыдущими. KV Cache сохраняет Key и Value "
    "для предыдущих токенов, чтобы не вычислять их заново.", S["Body"]))
story.append(code_block(
    "Без KV Cache:  генерация N токенов → O(N²) attention вычислений\n"
    "С KV Cache:    генерация N токенов → O(N) attention вычислений\n"
    "\n"
    "Цена: память GPU растёт линейно с длиной контекста"))

story.append(Paragraph("Grouped-Query Attention (GQA)", S["H2"]))
story.append(Paragraph(
    "Используется в LLaMA-2/3. Разделяет Q-головы на группы, "
    "использующие общие K и V. Уменьшает размер KV Cache и ускоряет "
    "инференс без заметной потери качества.", S["Body"]))

story.append(key_takeaways([
    "MoE: несколько экспертов, роутер выбирает — больше ёмкость при той же скорости",
    "Flash Attention: 2-4x ускорение, меньше памяти",
    "KV Cache: O(N²) → O(N) для генерации",
    "GQA: уменьшает KV Cache, ускоряет инференс",
]))

story.append(Spacer(1, 10 * mm))
story.append(HRFlowable(width="100%", thickness=0.8, color=ACCENT, spaceAfter=6))
story.append(Paragraph(
    "Конец Книги 3. Следующая — Книга 4: Практическое применение ИИ.",
    S["Caption"]))

build_book(
    "Kniga-3-Arkhitektura-Neirosetey-i-Transformerov.pdf",
    "Библиотека ИИ",
    "Архитектура нейросетей",
    "K3",
    story,
    "Библиотека ИИ · Книга 3 · Архитектура",
)
print("Книга 3 построена.")
