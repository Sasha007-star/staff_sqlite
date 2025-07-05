import sqlite3
import json
from datetime import datetime

# 🔧 Безпечний парсер дат (під SQL формат)
def parse_date_safe(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

# 📂 Підключення до SQLite-бази
conn = sqlite3.connect("staff.db")
cursor = conn.cursor()

# ✅ Увімкнення зовнішніх ключів
cursor.execute("PRAGMA foreign_keys = ON;")

# 🧱 Створення таблиці staff
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    nationality TEXT,
    gender TEXT,
    office_number INTEGER,
    accessment REAL
);
""")

# 🧱 Створення таблиці employment
cursor.execute("""
CREATE TABLE IF NOT EXISTS employment (
    employment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER,
    employment_date DATE,
    graduation_date DATE,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
);
""")

# 📥 Завантаження даних із JSON
with open("staff_data.json", "r", encoding="utf-8") as f:
    staff_data = json.load(f)

# ➕ Вставка кожного запису
for person in staff_data:
    # 👤 Додавання до staff
    cursor.execute("""
        INSERT INTO staff (
            first_name, last_name, date_of_birth, nationality, gender,
            office_number, accessment
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        person["first_name"],
        person["last_name"],
        parse_date_safe(person["date_of_birth"]),
        person["nationality"],
        person["gender"],
        person["office_number"],
        person["accessment"]
    ))

    staff_id = cursor.lastrowid

    # 💼 Додавання до employment
    cursor.execute("""
        INSERT INTO employment (
            staff_id, employment_date, graduation_date
        )
        VALUES (?, ?, ?)
    """, (
        staff_id,
        parse_date_safe(person.get("employment_date")),
        parse_date_safe(person.get("graduation_date"))
    ))

# 💾 Завершення
conn.commit()
conn.close()

print("✅ Дані успішно додано до бази даних.")

