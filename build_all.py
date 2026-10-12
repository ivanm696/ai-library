#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка всех PDF-книг библиотеки ИИ.

Запуск:
    python build_all.py           # все книги + каталог
    python build_all.py 1 3       # только книги 1 и 3
"""
import sys
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "pdf")

BOOKS = {
    "0": ("book0_catalog",       "Каталог библиотеки"),
    "1": ("book1_basics",        "Основы ИИ"),
    "2": ("book2_prompt",        "Промпт-инжиниринг"),
    "3": ("book3_architecture",  "Архитектура нейросетей"),
    "4": ("book4_practical",     "Практическое применение"),
    "5": ("book5_ethics",        "Этика и безопасность"),
}

def main():
    args = sys.argv[1:]
    keys = [a for a in args if a in BOOKS] if args else list(BOOKS.keys())

    if not keys:
        print("Неверный аргумент. Доступные: " + ", ".join(BOOKS))
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Передаём output_dir через переменную окружения
    os.environ["AI_LIBRARY_OUTPUT_DIR"] = OUTPUT_DIR

    print(f"Сборка {len(keys)} книг → {OUTPUT_DIR}/\n")

    success = []
    failed = []

    for key in keys:
        module_name, title = BOOKS[key]
        print(f"[Книга {key}] {title}...")
        try:
            mod = __import__(module_name)
            # book_engine.build_book вызывается внутри модуля,
            # но без output_dir. Переберём и вызовем заново?
            # Нет — модуль уже вызвал build_book с фиксированным именем.
            # Вместо этого: импортируем, и модуль сам создаст PDF
            # в текущей директории. Потом переместим.
            success.append(key)
        except Exception as e:
            print(f"  ✗ ОШИБКА: {e}")
            failed.append((key, str(e)))

    # Перемещаем PDF в выходную папку
    import shutil
    import glob
    for pdf in glob.glob(os.path.join(os.path.dirname(__file__), "Kniga-*.pdf")):
        dest = os.path.join(OUTPUT_DIR, os.path.basename(pdf))
        shutil.move(pdf, dest)

    print(f"\n{'='*50}")
    print(f"Успешно: {len(success)} | Ошибок: {len(failed)}")
    if failed:
        for key, err in failed:
            print(f"  Книга {key}: {err}")
    print(f"PDF сохранены в: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
