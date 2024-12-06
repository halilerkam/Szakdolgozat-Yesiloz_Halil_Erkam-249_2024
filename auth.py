# auth.py
import mysql.connector
import session
import bcrypt

def register_user(firstname, lastname, email, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="todo_app",
            autocommit = True
        )
        cursor = connection.cursor()

        def hash_password(password: str) -> str:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed_password.decode('utf-8')

        check_email_query = "SELECT COUNT(*) FROM felhasznalok WHERE email = %s"
        cursor.execute(check_email_query, (email,))
        result = cursor.fetchone()

        if result[0] > 0:
            return False
        
        hashed_password = hash_password(password)

        insert_query = "INSERT INTO felhasznalok (keresztnev, vezeteknev, email, jelszo) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (firstname, lastname, email, hashed_password))
        
        connection.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def login_user(email, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="todo_app",
            autocommit = True
        )
        cursor = connection.cursor()

        query = "SELECT id, jelszo FROM felhasznalok WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user is None:
            return False
        hashed_password = user[1]
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return False  # Hibás jelszó
        session.set_current_user_id(user[0])
        return True

    except mysql.connector.Error as err:
        print(f"Adatbázis hiba: {err}")
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


