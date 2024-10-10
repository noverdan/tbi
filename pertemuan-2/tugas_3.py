from mysql.connector import Error
import mysql.connector
from tugas_2 import NotCaseSensitive

config = {
        "host": "mysql-students-my-student-projects.h.aivencloud.com",
        "port": "13993",
        "user": "galangarsandy",
        "password": "AVNS_1coj2um74BOgK_AGXaI", # Password berlaku s/d tgl 11-Okt-24, jgn nackal Ya Mas Brow✌️
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
    
    def __del__(self):
        self.connection.close()
        
db = DatabaseConnection()
list_mahasiswa = db.Select("SELECT nim, nama FROM mahasiswa")

inverted_index = NotCaseSensitive()
list_mahasiswa_inverted = inverted_index.create_inverted_index(list_mahasiswa)

keywords = input("Masukan Nama Mahasiswa: ")

if not keywords:
    print("Ups Data Nama kosong! Tidak bisa dilakukan pencarian")
    exit()
search_result = inverted_index.search(keywords)
print(f"{len(search_result)} NIM ditemukan dari hasil pencarian '{keywords}': {search_result}")