import psycopg2
from psycopg2 import OperationalError, Error

def create_tables():
    try:
        conn = psycopg2.connect(
            dbname="postgres", 
            user="postgres", 
            password="0000", 
            host="localhost", 
            port="5432"
        )
        cursor = conn.cursor()
        
        # Створення таблиці users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        """)

        # Створення таблиці status
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed')
        ON CONFLICT (name) DO NOTHING;
        """)

        # Створення таблиці tasks
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER NOT NULL REFERENCES status(id),
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        
        conn.commit()
        print("Таблиці успішно створено.")
    except OperationalError as e:
        print("Не вдалось з'єднатись з базою даних:", e)
    except Error as e:
        print("SQL помилка:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_tables()