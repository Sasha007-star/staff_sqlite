import sqlite3
import json
from datetime import datetime

def parse_date_safe(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

conn = sqlite3.connect("staff.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    nationality TEXT,
    gender TEXT,
    office_number INTEGER
    accessment REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employment (
    employment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER,
    employment_date DATE,
    graduation_date DATE,
    FOREIGN KEY (staff_id) REFERENCES staffs(staff_id) ON DELETE CASCADE
);
""")

with open("", "r", encoding="utf-8"
) as f:
    staffs = json.load(f)

for staff in staffs:
    cursor.execute("""
        INSERT INTO staffs (
            first_name, last_name, date_of_birth, nationality, gender, office_number, accessment
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        staff["first_name"],
        staff["last_name"],
        parse_date_safe(staff["date_of_birth"]),
        staff["nationality"],
        staff["gender"],
        staff["office_number"],
        staff["accessment"]
))
    
staff_id = cursor.lastrowid

cursor.execute("""
    INSERT INTO employment (staff_id, employment_date, graduation_date)
    VALUES (?, ?, ?)
""", (
    staff_id,
    parse_date_safe(staff.get("employment_date")),
    parse_date_safe(staff.get("graduation_date"))
))

conn.commit()
conn.close()

print("Дані успішно додано до бази даних.")
