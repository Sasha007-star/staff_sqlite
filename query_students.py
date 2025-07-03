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
    ORDER BY accessment DESC
    LIMIT 3
""")

print("\n Працівники у яких успішність така, що вони на межі вигнання з роботи")

execute_query("""
    SELECT first_name, last_name, accessment
    FROM staff
    WHERE accessment < '3.7'
""")

print("\n Працівники що народилися в 1900 роках і за гендером чоловік")

execute_query("""
    SELECT first_name, last_name, date_of_birth, gender
    FROM staff
    WHERE gender = 'чоловік' AND date_of_birth LIKE '19________'
""")

print("\n Хай програма перевірить який працівник що має хорошу успішність, в 154 чи 110 офісному кабінеті")

execute_query("""
    SELECT first_name, last_name, office_number, gender, accessment
    FROM staff
    WHERE office_number = 110 OR office_number = 154
    ORDER BY accessment DESC
""")

print("\n Працівники що вступили на роботу в 2000-х роках і вони мають середню успішність")

execute_query("""
    SELECT first_name, last_name, employment_date, accessment
    FROM staff, employment
    WHERE employment_date LIKE '2010______'
    ORDER BY accessment DESC
""")

print("\n Працівники які народилися між 2010-2021-х роках")

execute_query("""
    SELECT first_name, last_name, accessment
    FROM staff
    WHERE accessment BETWEEN 4 AND 4.9
""")

print("\n Показ яка у кого успішність ")

execute_query("""
    SELECT first_name, last_name, accessment
    FROM staff
    GROUP BY accessment
""")
