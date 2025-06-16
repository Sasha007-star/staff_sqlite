import sqlite3
import json
from datetime import datetime

DB_NAME = "staff.db"
INPUT_JSON = "staff_data.json"
OUTPUT_JSON = "exported_staff.json"

def parse_date_safe(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def create_tables(cursor):
    cursor.execute("PRAGMA foreign_keys = ON;")

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employment (
        employment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id INTEGER,
        employment_date DATE,
        graduation_date DATE,
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
    );
    """)

def insert_data(cursor, staffs):
    for staff in staffs:
        cursor.execute("""
            INSERT INTO staff (
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

def export_to_json(cursor):
    cursor.execute("SELECT * FROM staff")
    staff_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM employment")
    employment_rows = cursor.fetchall()

    staff_list = []
    for staff in staff_rows:
        staff_dict = {
            "staff_id": staff[0],
            "first_name": staff[1],
            "last_name": staff[2],
            "date_of_birth": staff[3],
            "nationality": staff[4],
            "gender": staff[5],
            "office_number": staff[6],
            "accessment": staff[7],
        }

        employment = next((e for e in employment_rows if e[1] == staff[0]), None)
        if employment:
            staff_dict["employment_date"] = employment[2]
            staff_dict["graduation_date"] = employment[3]
        else:
            staff_dict["employment_date"] = None
            staff_dict["graduation_date"] = None

        staff_list.append(staff_dict)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(staff_list, f, ensure_ascii=False, indent=4)

    print(f"✅ Дані експортовано у {OUTPUT_JSON}")

def main():
    # 1. Зчитування JSON-даних
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        staffs = json.load(f)

    # 2. Підключення до бази та створення таблиць
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    create_tables(cursor)

    # 3. Додавання даних
    insert_data(cursor, staffs)

    conn.commit()

    # 4. Експорт у JSON
    export_to_json(cursor)

    conn.close()
    print("✅ Дані успішно збережено в базу та експортовано!")

if __name__ == "__main__":
    main()
