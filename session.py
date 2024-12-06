# session.py
import mysql.connector
import database_helper as dbh

current_user_id = None
current_user = None

class User:
    def __init__(self, user_id, first_name, last_name, email, password, points):
        self.user_id = user_id  # Felhasználói ID
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.points = points

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.points} ({self.email}, {self.password})"


def set_current_user_id(user_id):
    global current_user_id
    current_user_id = user_id

def get_current_user_data(user_id):
    conn = mysql.connector.connect(
        host="localhost",  
        user="root",  
        password="",  
        database="todo_app",
        autocommit = True
    )
    cursor = conn.cursor()
    
    # Query the database to get the user by email
    cursor.execute("SELECT * FROM felhasznalok WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()  # Fetch the first matching user (if any)
    
    conn.close()
    if user_data:
        # Az oszlopok nevére és azok indexére kell hivatkozni
        user_id = user_data[0]  # user_id oszlop (általában az első)
        first_name = user_data[1]  # first_name oszlop
        last_name = user_data[2]  # last_name oszlop
        email = user_data[3]  # email oszlop
        password = user_data[4]
        points = user_data[5]

        # User objektum létrehozása
        current_user = User(user_id, first_name, last_name, email, password, points)
        return current_user
    else:
        return None  # Ha nincs találat
    
def logout():
    global current_user
    current_user = None

    global current_user_id
    current_user_id = None