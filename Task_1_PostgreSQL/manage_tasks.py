import psycopg2

def run_queries():
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="0000", 
        host="localhost", 
        port="5432"
    )
    cursor = conn.cursor()
   
    # Запит 1: Отримати всі завдання певного користувача
    user_id = 1
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
    print("Завдання для користувача 1:", cursor.fetchall())

    # Запит 2: Вибрати завдання за певним статусом 'new'
    cursor.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');")
    print("Завдання зі статусом 'new':", cursor.fetchall())

    # Запит 3: Оновити статус конкретного завдання
    task_id_to_update = 1
    cursor.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = %s;", (task_id_to_update,))
    conn.commit()
    print(f"Статус завдання {task_id_to_update} оновлено на 'in progress'.")

    # Запит 4: Отримати список користувачів, які не мають жодного завдання
    cursor.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);")
    print("Користувачі без завдань:", cursor.fetchall())

    # Запит 5: Додати нове завдання для конкретного користувача
    cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New Task', 'Description here', (SELECT id FROM status WHERE name = 'new'), 1);")
    conn.commit()
    print("Нове завдання для користувача 1 додано.")

    # Запит 6: Отримати всі завдання, які ще не завершено
    cursor.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');")
    print("Завдання, які не завершено:", cursor.fetchall())

    # Запит 7: Видалити конкретне завдання
    task_id_to_delete = 2
    cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id_to_delete,))
    conn.commit()
    print(f"Завдання {task_id_to_delete} видалено.")

    # Запит 8: Знайти користувачів з певною електронною поштою
    email_search = "%@gmail.com"
    cursor.execute("SELECT * FROM users WHERE email LIKE %s;", (email_search,))
    print("Користувачі з Gmail:", cursor.fetchall())

    # Запит 9: Оновити ім'я користувача
    user_id_to_update = 1
    new_name = "Updated Name"
    cursor.execute("UPDATE users SET fullname = %s WHERE id = %s;", (new_name, user_id_to_update))
    conn.commit()
    print(f"Ім'я користувача {user_id_to_update} оновлено.")

    # Запит 10: Отримати кількість завдань для кожного статусу
    cursor.execute("SELECT s.name, COUNT(t.id) FROM status s LEFT JOIN tasks t ON s.id = t.status_id GROUP BY s.name;")
    print("Кількість завдань за статусами:", cursor.fetchall())

    # Запит 11: Отримати завдання, призначені користувачам з певною доменною частиною електронної пошти
    domain = "%@example.com"
    cursor.execute("SELECT t.* FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE %s;", (domain,))
    print("Завдання для користувачів з доменом @example.com:", cursor.fetchall())

    # Запит 12: Отримати список завдань, що не мають опису
    cursor.execute("SELECT * FROM tasks WHERE description IS NULL OR description = '';")
    print("Завдання без опису:", cursor.fetchall())

    # Запит 13: Вибрати користувачів та їхні завдання, що є у статусі 'in progress'
    cursor.execute("SELECT u.fullname, t.title FROM users u JOIN tasks t ON u.id = t.user_id WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress');")
    print("Користувачі та їхні завдання у статусі 'in progress':", cursor.fetchall())

    # Запит 14: Отримати користувачів та кількість їхніх завдань
    cursor.execute("SELECT u.fullname, COUNT(t.id) AS task_count FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.fullname;")
    print("Користувачі та кількість їхніх завдань:", cursor.fetchall())

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_queries()