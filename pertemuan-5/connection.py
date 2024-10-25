from mysql.connector import Error
import mysql.connector

config = {
        "host": "mysql-students-my-student-projects.h.aivencloud.com",
        "port": "13993",
        "user": "galangarsandy",
        "password": "AVNS_1coj2um74BOgK_AGXaI",
        "database": "quran"
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
    
    def __del__(self):
        self.connection.close()  