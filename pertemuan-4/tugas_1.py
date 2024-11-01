from mysql.connector import Error
import mysql.connector
from main import MyDocument

config = {
        "host": "mysql-students-my-student-projects.h.aivencloud.com",
        "port": "13993",
        "user": "galangarsandy",
        "password": "AVNS_1coj2um74BOgK_AGXaI",
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
"""
list_mahasiswa :
    ('1', 'Dewi Tri Astutui')
    ('2', 'Yulian Saputra')
    ('3', 'Muhammad Tegar Putra')
    ('4', 'Galang Arsandy')
    ('5', 'Noverdan Putra')
    ('6', 'Budi Sudarsono')
    ('7', 'Anton Tri Septo')
    ('8', 'Muhammad Galang')
    ('9', 'Moh Bayu Gatra ')
    ('10', 'Ayu Setiana Dewi')
    ('11', 'Putra Sihombing')
"""

document = MyDocument()
for nim, nama in list_mahasiswa:
    document.add_inverted_index_doc(nim, nama)
    
print(document.bool_retrieval_search("+Putra -Muhammad +Galang"))