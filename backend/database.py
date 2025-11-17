import sqlite3
from datetime import datetime
import io
import csv

from openpyxl import Workbook

DB_PATH = "results.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Один респондент = одна строка, все ответы лежат в колонках q1..q39 + комментарии + q40 + total
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,

            -- Числовые ответы
            q1  INTEGER NOT NULL,
            q2  INTEGER NOT NULL,
            q3  INTEGER NOT NULL,
            q4  INTEGER NOT NULL,
            q5  INTEGER NOT NULL,
            q6  INTEGER NOT NULL,
            q7  INTEGER NOT NULL,
            q8  INTEGER NOT NULL,
            q9  INTEGER NOT NULL,
            q10 INTEGER NOT NULL,
            q11 INTEGER NOT NULL,
            q12 INTEGER NOT NULL,
            q13 INTEGER NOT NULL,
            q14 INTEGER NOT NULL,
            q15 INTEGER NOT NULL,
            q16 INTEGER NOT NULL,
            q17 INTEGER NOT NULL,
            q18 INTEGER NOT NULL,
            q19 INTEGER NOT NULL,
            q20 INTEGER NOT NULL,
            q21 INTEGER NOT NULL,
            q22 INTEGER NOT NULL,
            q23 INTEGER NOT NULL,
            q24 INTEGER NOT NULL,
            q25 INTEGER NOT NULL,
            q26 INTEGER NOT NULL,
            q27 INTEGER NOT NULL,
            q28 INTEGER NOT NULL,
            q29 INTEGER NOT NULL,
            q30 INTEGER NOT NULL,
            q31 INTEGER NOT NULL,
            q32 INTEGER NOT NULL,
            q33 INTEGER NOT NULL,
            q34 INTEGER NOT NULL,
            q35 INTEGER NOT NULL,
            q36 INTEGER NOT NULL,
            q37 INTEGER NOT NULL,
            q38 INTEGER NOT NULL,
            q39 INTEGER NOT NULL,

            -- Текстовые комментарии (в форме q17.1, q19.1 и т.д.)
            q17_1 TEXT,
            q19_1 TEXT,
            q30_1 TEXT,
            q31_1 TEXT,
            q32_1 TEXT,
            q33_1 TEXT,
            q35_1 TEXT,
            q38_1 TEXT,
            q39_1 TEXT,

            -- Свободный текст
            q40   TEXT,

            -- Суммарный балл (например, сумма q4–q39)
            total INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_results(answers):
    """
    answers — объект, у которого есть атрибуты q1..q39, q17_1, ..., q39_1, q40.
    Идеально подходит твой Pydantic-класс TestAnswers.
    """

    # Например: считаем total как сумму шкал 4–39 (q1, q2, q3 — возраст, выслуга, категория)
    total = sum(getattr(answers, f"q{i}") for i in range(4, 40))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Список полей в том же порядке, как в таблице (кроме id)
    numeric_fields = [f"q{i}" for i in range(1, 40)]  # q1..q39

    text_fields = [
        "q17_1",
        "q19_1",
        "q30_1",
        "q31_1",
        "q32_1",
        "q33_1",
        "q35_1",
        "q38_1",
        "q39_1",
        "q40",
    ]

    all_fields = numeric_fields + text_fields

    placeholders = ", ".join(["?"] * (len(all_fields) + 2))  # + created_at + total
    columns = ", ".join(["created_at"] + all_fields + ["total"])

    values = [datetime.now().isoformat()]
    # Числовые ответы
    for name in numeric_fields:
        values.append(getattr(answers, name))
    # Текстовые, могут быть None
    for name in text_fields:
        values.append(getattr(answers, name, None))

    values.append(total)

    cur.execute(
        f"INSERT INTO results ({columns}) VALUES ({placeholders})",
        values,
    )

    conn.commit()
    conn.close()


def get_results():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Берём всю строку (id, created_at, все q*, total)
    cur.execute("""
        SELECT *
        FROM results
        ORDER BY id
    """)
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_csv_results():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM results
        ORDER BY id
    """)
    rows = cur.fetchall()
    headers = [desc[0] for desc in cur.description]
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(headers)
    writer.writerows(rows)
    output.seek(0)

    return output


def get_xlsx_results():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM results
        ORDER BY id
    """)
    rows = cur.fetchall()
    headers = [desc[0] for desc in cur.description]
    conn.close()

    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    # Заголовки
    ws.append(headers)

    # Данные
    for row in rows:
        ws.append(list(row))

    wb.save(output)
    output.seek(0)

    return output
