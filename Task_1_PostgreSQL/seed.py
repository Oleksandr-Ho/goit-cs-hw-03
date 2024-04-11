import psycopg2
from faker import Faker
import random

def seed_database():
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="0000", 
        host="localhost", 
        port="5432"
    )
    cursor = conn.cursor()
    fake = Faker()

    # Генерація даних для таблиці 'users'
    users_inserted = []
    for _ in range(100):  # Генеруємо 100 користувачів
        fullname = fake.name()
        email = fake.unique.email()
        if email not in users_inserted:  # Переконуємось, що email є унікальним
            cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s);", (fullname, email))
            users_inserted.append(email)

    # Генерація даних для таблиці 'tasks'
    cursor.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(200):  # Генеруємо 200 завдань
        title = fake.sentence()
        description = fake.paragraph()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);", (title, description, status_id, user_id))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    seed_database()
