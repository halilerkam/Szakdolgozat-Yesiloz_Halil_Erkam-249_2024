import mysql.connector
import tkinter.messagebox as messagebox
import session
import bcrypt
import json
import sys
import os

has_changed = 0

APP_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

CONFIG_FILE_NAME = "db_config.json"
CONFIG_PATH = os.path.join(APP_DIR, CONFIG_FILE_NAME)
print(CONFIG_PATH)

if not os.path.exists(CONFIG_PATH):
    default_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "todo_app"
    }
    with open(CONFIG_PATH, 'w') as config_file:
        json.dump(default_config, config_file, indent=4)
    print(f"A konfigurációs fájl létrehozva: {CONFIG_PATH}")

with open(CONFIG_PATH, 'r') as config_file:
    config = json.load(config_file)

class DatabaseHelper:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                autocommit=True
            )
            self.cursor = self.connection.cursor()
            print(f"Connection successful: {self.connection}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None
            self.cursor = None

    def check_connection(self):
        if self.connection == None:
            return False
        else:
            return True

    def add_task(self, user_id, title, description, date, location, priority, environment, invities_list):
        query = "INSERT INTO feladatok (user_id, title, description, date, location, priority, environment) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (user_id, title, description, date, location, priority, environment)
        self.cursor.execute(query, values)
        self.connection.commit()

        task_id = self.cursor.lastrowid

        self.cursor.execute("INSERT INTO feladat_meghivottak (task_id, user_id, is_creator) VALUES (%s, %s, TRUE)", (task_id, user_id))
        self.connection.commit()

        for invitie in invities_list:
            self.cursor.execute("INSERT INTO feladat_meghivottak (task_id, user_id, is_creator) VALUES (%s, %s, FALSE)", (task_id, invitie))
            self.connection.commit()
        check_query = "SELECT COUNT(*) FROM feladat_meghivottak WHERE task_id = %s"
        self.cursor.execute(check_query, (task_id,))
        exists = self.cursor.fetchone()[0]

        # Ha a task_id még nem szerepel, beszúrunk egy másik sort is, ahol is_creator TRUE
        if exists == 0:
            insert_creator_query = "INSERT INTO feladat_meghivottak (task_id, user_id, is_creator) VALUES (%s, %s, TRUE)"
            self.cursor.execute(insert_creator_query, (task_id, session.current_user_id))

    def add_invities(self, task_id, invities_list):
        for invitie in invities_list:
            self.cursor.execute("INSERT INTO feladat_meghivottak (task_id, user_id, is_creator) VALUES (%s, %s, FALSE)", (task_id, invitie))
            self.connection.commit()
        
    def remove_invities(self, task_id, invities_list):
        for invitie in invities_list:
            self.cursor.execute("DELETE FROM feladat_meghivottak WHERE task_id = %s AND user_id = %s", (task_id, invitie))
            self.connection.commit()

    def remove_from_collab(self, task_id):
        query = "DELETE FROM feladat_meghivottak WHERE task_id = %s AND user_id = %s"
        values = (task_id, session.current_user_id)
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_task(self, task_id):
        query = "DELETE FROM feladatok WHERE id = %s"
        self.cursor.execute(query, (task_id,))
        self.connection.commit()

    def task_done(self, task_id):
        query = f"UPDATE feladatok SET is_completed = 1 WHERE id = %s;"
        self.cursor.execute(query, (task_id,))
        self.connection.commit()

    def task_undone(self, task_id):
        query = f"UPDATE feladatok SET is_completed = 0 WHERE id = %s;"
        self.cursor.execute(query, (task_id,))
        self.connection.commit()

    def get_all_done_tasks(self):
        if session.current_user_id != None:
            query = "SELECT * FROM feladatok WHERE user_id = %s AND is_completed = 1 AND id NOT IN (SELECT task_id FROM feladat_meghivottak WHERE task_id IS NOT NULL GROUP BY task_id HAVING COUNT(*) > 1) ORDER BY date ASC"
            self.cursor.execute(query, (session.current_user_id,))
            tasks = self.cursor.fetchall()
            return tasks
    
    def get_all_done_collab_tasks(self):
        if session.current_user_id != None:
            query = "SELECT * FROM feladatok WHERE is_completed = 1 AND id IN (SELECT task_id FROM feladat_meghivottak WHERE user_id = %s) ORDER BY date ASC"
            self.cursor.execute(query, (session.current_user_id,))
            done_collab_tasks = self.cursor.fetchall()
            return done_collab_tasks
        
    def get_invities(self, task_id):
        query = "SELECT user_id FROM feladat_meghivottak WHERE task_id = %s AND is_creator = 0"
        self.cursor.execute(query, (task_id,))
        invities = None
        invities = self.cursor.fetchall()
        return invities
    
    def reward_points(self, task_id):
        query_resztvevok = "SELECT COUNT(*) AS resztvevok_szama FROM feladat_meghivottak WHERE task_id = %s"
        self.cursor.execute(query_resztvevok, (task_id,))
        resztvevok_szama = self.cursor.fetchone()[0]
        pont = resztvevok_szama
        if pont >=2:
            query_update = "UPDATE felhasznalok SET points = points + %s WHERE id IN (SELECT user_id FROM feladat_meghivottak WHERE task_id = %s)"
            self.cursor.execute(query_update, (pont, task_id))
            self.connection.commit()
    
    def revoke_points(self, task_id):
        self.cursor.execute("SELECT user_id FROM feladat_meghivottak WHERE task_id = %s;", (task_id,))
        participants = self.cursor.fetchall()
        participant_count = len(participants)
        if participant_count > 0:
            for participant in participants:
                user_id = participant[0]
                self.cursor.execute("UPDATE felhasznalok SET points = GREATEST(points - %s, 0) WHERE id = %s;", (participant_count, user_id))
            self.connection.commit()
        
    def get_current_points(self):
        self.cursor.execute("SELECT points FROM felhasznalok WHERE id = %s;", (session.current_user_id,))
        points = self.cursor.fetchone()[0]
        return points
        

    
    def update_task(self, changes, task_id):
        db_columns = ["title", "description", "date", "location", "priority", "environment"]
        for change in changes:
            column_to_update = db_columns[change[0]]
            print(column_to_update)
            print(change[1])
            query = f"UPDATE feladatok SET {column_to_update} = %s WHERE id = %s;"
            values = (change[1], task_id)
            self.cursor.execute(query, values)
        self.connection.commit()

    
    def get_all_tasks(self):
        if session.current_user_id != None:
            query = "SELECT * FROM feladatok WHERE user_id = %s AND is_completed != 1 AND id NOT IN (SELECT task_id FROM feladat_meghivottak WHERE task_id IS NOT NULL GROUP BY task_id HAVING COUNT(*) > 1) ORDER BY date ASC"
            self.cursor.execute(query, (session.current_user_id,))
            tasks = self.cursor.fetchall()
            print(tasks)
            return tasks
        
    def get_collab_tasks(self):
        if session.current_user_id != None:
            query = "SELECT * FROM feladatok WHERE is_completed != 1 AND id IN (SELECT task_id FROM feladat_meghivottak GROUP BY task_id HAVING COUNT(*) >= 2) ORDER BY date ASC"
            self.cursor.execute(query)
            collab_tasks = self.cursor.fetchall()
            print(collab_tasks)
            return collab_tasks
        
    def is_creator(self, task_id):
        if session.current_user_id != None:
            query = "SELECT * FROM feladatok WHERE id IN (SELECT task_id FROM feladat_meghivottak WHERE task_id = %s AND user_id = %s AND is_creator = 1)"
            self.cursor.execute(query, (task_id, session.current_user_id,))
            collab_tasks = self.cursor.fetchall()
            return collab_tasks
        
    def get_single_tasks(self, task_id):
        if session.current_user_id != None:
            query = "SELECT * FROM feladatok WHERE id = %s"
            self.cursor.execute(query, (task_id,))
            task = self.cursor.fetchone()
            return task

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


    def update_password(self, user_id, new_password):
        if session.current_user_id != None:
            if user_id == session.current_user_id:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                query = f"UPDATE felhasznalok SET jelszo = %s WHERE id = %s;"
                values = (hashed_password, user_id)
                self.cursor.execute(query, values)
                self.connection.commit()
                return True
            else:
                return False
        else:
            return False
    

    def send_friend_request(self, sender_id, receiver_email):
        query = "SELECT id FROM felhasznalok WHERE email = %s;"
        self.cursor.execute(query, (receiver_email,))
        receiver = self.cursor.fetchone()
        if receiver:
            receiver_id = receiver[0]
            query = "INSERT INTO barati_felkeresek (kuldte, fogadta, allapot) VALUES (%s, %s, 'függőben');"
            self.cursor.execute(query, (sender_id, receiver_id))
            self.connection.commit()
            return True
        else:
            print("Nincs ilyen email-című felhasználó.")
            return False

    def get_friends(self, user_id):
        query = " SELECT f.id FROM baratok b JOIN felhasznalok f ON (b.felhasznalo_1 = f.id OR b.felhasznalo_2 = f.id) WHERE (%s IN (b.felhasznalo_1, b.felhasznalo_2)) AND f.id != %s ORDER BY f.email ASC;"
        self.cursor.execute(query, (user_id, user_id))
        data = self.cursor.fetchall()
        return data
    
    def get_requests(self, user_id):
        query = "SELECT f.id, f.email, f.points FROM barati_felkeresek bf JOIN felhasznalok f ON bf.kuldte = f.id WHERE bf.fogadta = %s AND bf.allapot = 'függőben' ORDER BY bf.kuldve DESC;"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_friend_data(self, friend_id):
        query = "SELECT * FROM felhasznalok WHERE id = %s"
        self.cursor.execute(query, (friend_id,))
        return self.cursor.fetchall()
    
    def unfriend(self, friend_id):
        query = "DELETE FROM baratok WHERE (felhasznalo_1 = %s AND felhasznalo_2 = %s) OR (felhasznalo_1 = %s AND felhasznalo_2 = %s)"
        values = (session.current_user_id, friend_id, friend_id, session.current_user_id)        
        self.cursor.execute(query, values)
        self.connection.commit()
    
    def accept_friend_request(self, sender_id):
        query_update_status = "UPDATE barati_felkeresek SET allapot = 'elfogadva' WHERE kuldte = %s AND fogadta = %s;"
        query_add_to_friends = "INSERT INTO baratok (felhasznalo_1, felhasznalo_2) VALUES (%s, %s);"
        try:
            self.cursor.execute(query_update_status, (sender_id, session.current_user_id))
            self.cursor.execute(query_add_to_friends, (session.current_user_id, sender_id))
            self.connection.commit()
        except Exception as e:
            print(f"Hiba történt a barátkérés elfogadásakor: {e}")
            self.connection.rollback()
    
    def deny_friend_request(self, sender_id):
        query_delete_request = "DELETE FROM barati_felkeresek WHERE kuldte = %s AND fogadta = %s;"
        try:
            self.cursor.execute(query_delete_request, (sender_id, session.current_user_id))
            self.connection.commit()
        except Exception as e:
            print(f"Hiba történt a barátkérés elutasításakor: {e}")
            self.connection.rollback()
    

    def get_friends_for_task(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM baratok")
        return cursor.fetchall()

    def get_friend_details_by_ids(self, ids):
        cursor = self.connection.cursor()
        query = "SELECT id, name FROM friends WHERE id IN (%s)" % ','.join(['%s'] * len(ids))
        cursor.execute(query, ids)
        return cursor.fetchall()
    

    def get_city_date_pairs(self):
            query = "SELECT id, location, date FROM feladatok WHERE environment = 'Kültéri tevékenység' AND date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 5 DAY)"

            self.cursor.execute(query)
            result = self.cursor.fetchall()

            city_date_pairs = []
            for row in result:
                id = row[0]
                city = row[1]
                task_date = row[2]
                city_date_pairs.append({"id": id, "city": city, "date": task_date})

            return city_date_pairs
    
    def get_city_date_pairs_single(self, task_id):
            query = "SELECT id, location, date FROM feladatok WHERE environment = 'Kültéri tevékenység' AND date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 5 DAY)"

            self.cursor.execute(query)
            result = self.cursor.fetchall()

            city_date_pairs = []
            for row in result:
                id = row[0]
                city = row[1]
                task_date = row[2]
                city_date_pairs.append({"id": id, "city": city, "date": task_date})

            return city_date_pairs