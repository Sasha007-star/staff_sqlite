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

print("\nДістаємо всі дані з таблиці 'staff'")

execute_query("""
    SELECT *
    FROM staff
""")

print("\nДістаємо колонки 'date_of_birth', 'office_number' з таблиці 'staff'")

execute_query("""
    SELECT date_of_birth, office_number
    FROM staff
""")

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
    WHERE last_name LIKE '____yk'
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
    WHERE nationality = 'Ukraine'
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
    WHERE gender = 'Male' AND date_of_birth LIKE '19________'
""")

print("\n Хай програма перевірить який працівник що має хорошу успішність, в 770 чи 863 офісному кабінеті")

execute_query("""
    SELECT first_name, last_name, office_number, gender, accessment
    FROM staff
    WHERE office_number = 770 OR office_number = 863
    ORDER BY accessment DESC
""")

print("\n Працівники що вступили на роботу в 2003-х роках і вони мають середню успішність")

execute_query("""
    SELECT first_name, last_name, employment_date, accessment
    FROM staff, employment
    WHERE employment_date LIKE '2003______'
    ORDER BY accessment DESC
    LIMIT 5
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

print("\nДістаємо всі номера офісних кабінетів працівників крім кабінета 101")

execute_query("""
    SELECT first_name, last_name, office_number
    FROM staff
    WHERE NOT office_number = '101'
""")

print("\nДістаємо 5 працівників із успішністю 4.62, 3.79, 3.89")

execute_query("""
    SELECT first_name, accessment
    FROM staff
    WHERE accessment IN('4.62', '3.79', '3.89')
""")