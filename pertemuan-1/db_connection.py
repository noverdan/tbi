from mysql.connector import Error
import mysql.connector

config = {
        "host": "mysql-students-my-student-projects.h.aivencloud.com",
        "port": "13993",
        "user": "galangarsandy",
        "password": "AVNS_hg0Rmr0qw5OGpgHkNKM", # Password berlaku s/d tgl 3-Okt-24, jgn nackal Ya Mas Brow✌️
        "database": "db_tbi_amikom"
    }

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
            print("Connected to the database")
        except Error as err:
            print(f"The error '{err}' occurred")
            
    def Select(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Error as err:
            print(f"Select data ERROR: ", err)
        finally:
            print("Select data Done")
    
    def Insert(self, sql, val):
        try:
            self.cursor.execute(sql, val)
            self.connection.commit()
        except Error as err:
            print(f"Insert data ERROR: ", err)
        finally:
            print("Insert data Done")
    def Delete(self, sql, val):
        try:
            self.cursor.execute(sql, val)
            self.connection.commit()
        except Error as err:
            print(f"Delete data ERROR: ", err)
        finally:
            print("Delete data Done")
    def __del__(self):
        # self.cursor.close()
        self.connection.close()
