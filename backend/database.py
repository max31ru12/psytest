import sqlite3
from datetime import datetime
import io
import csv

from openpyxl import Workbook

DB_PATH = "results.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            division TEXT NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_results(division, total):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO results (division, total, created_at)
        VALUES (?, ?, ?)
    """, (division, total, datetime.now()))

    conn.commit()
    conn.close()


def get_results():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # чтобы получать строки как dict-подобные объекты
    cur = conn.cursor()

    cur.execute("""
        SELECT id, division, total, created_at
        FROM results
        ORDER BY id
    """)
    rows = cur.fetchall()
    conn.close()

    # Переводим в список обычных dict'ов
    return [dict(row) for row in rows]


def get_csv_results():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, division, total, created_at
        FROM results
        ORDER BY id
    """)
    rows = cur.fetchall()
    headers = [desc[0] for desc in cur.description]
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')  # ; удобно для русской локали
    writer.writerow(headers)
    writer.writerows(rows)
    output.seek(0)

    return output


def get_xlsx_results():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, division, total, created_at
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

    # Сохраняем книгу в байтовый поток
    wb.save(output)
    output.seek(0)

    return output
