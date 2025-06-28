import sqlite3

conn = sqlite3.connect("staff.db")
cursor = conn.cursor()

def execute_query(query, params=()):
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Помилка при виконанні запиту: {e}")

print("\nІмена та прізвища студентів в алфавітному порядку")

execute_query("""
    SELECT first_name, last_name
    FROM staff
    ORDER BY first_name ASC
""")

print("\nВсі працівники з однаковим прізвищем але імена різні")

execute_query("""
    SELECT first_name, last_name
    FROM staff
    WHERE last_name LIKE '_____ук'
""")

print("\nПрацівники які ще працюють")

execute_query("""
    SELECT first_name, last_name, graduation_date
    FROM staff
    INNER JOIN employment 
    ON staff.staff_id = employment.staff_id
    WHERE graduation_date is NULL
""")

print("\n 3 працівників у яких середня успішність і вони з України ")

execute_query("""
    SELECT first_name, last_name, accessment, nationality
    FROM staff
    WHERE nationality LIKE 'Україн___'
    ORDER BY accessment ASC
    LIMIT 3
""")

print("\n Працівники у яких успішність ")