# Start Import Library
import mysql.connector # Import mysql.connector
from mysql.connector import Error # Import Error from mysql.connector
import re # Regular Expression
import numpy as np # Numerical Python (Numpy)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory # Sastrawi Stemmer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory # Sastrawi Stopword Remover
from nltk.tokenize import word_tokenize # Natural Language Toolkit (NLTK)
from sklearn.feature_extraction.text import TfidfVectorizer # Term Frequency-Inverse Document Frequency (TF-IDF)
from sklearn.metrics.pairwise import cosine_similarity # Cosine Similarity
# End Import Library

# Konfigurasi Database
db_config = {
        "host": "mysql-students-my-student-projects.h.aivencloud.com",
        "port": "13993",
        "user": "galangarsandy",
        "password": "AVNS_1coj2um74BOgK_AGXaI",
        "database": "quran"
    }
class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**db_config)
            self.cursor = self.connection.cursor()
            print("Connected to the database\n")
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

stemmer = StemmerFactory().create_stemmer() # Membuat objek stemmer
stopwords = StopWordRemoverFactory().create_stop_word_remover() # Membuat objek stopwords

db = DatabaseConnection() # Membuat objek database connection
data_quran = db.Select("SELECT * FROM id_indonesian limit 50") # Mengambil data dari database

corpus = [] # List untuk menampung data quran yang sudah di pre-processing

for (index, surat, ayat, text) in data_quran:
    pre_process = re.sub('[^a-zA-Z]', ' ', text.lower()) # Menghilaangkan karakter selain huruf a-z dan A-Z dan diubah menjadi spasi. Lalu diubah menjadi huruf kecil
    pre_process = re.sub(' +', ' ', pre_process) # Menghilangkan spasi yang berlebihan
    pre_process = stopwords.remove(pre_process) # Menghilangkan stopwords atau kata-kata yang tidak penting
    pre_process = stemmer.stem(pre_process) # Melakukan stemming atau mengubah kata-kata menjadi kata dasar
    
    corpus.append((index, surat, ayat, pre_process)) # Menambahkan data ke dalam list corpus
    
doc_vocabulary = set()
tokenized_documents = []

for (index, surat, ayat, text) in corpus:
    tokens = word_tokenize(text) # Tokenisasi kata atau memecah kalimat menjadi per kata
    tokens = [word.lower() for word in tokens if word.isalpha()] # Menghilangkan kata yang bukan alphabet, Misal tokens = ["Hello", "world!", "123", "Python3"] menjadi ["hello", "world", "python"]
    tokenized_documents.append(" ".join(tokens)) # Menambahkan kata-kata yang sudah di tokenisasi ke dalam list tokenized_documents
    doc_vocabulary.update(tokens) # Menambahkan kata-kata yang unik ke dalam set vocabulary, jadi tidak ada kata yang duplikat
    
vectorizer = TfidfVectorizer(vocabulary=doc_vocabulary) # Membuat objek vectorizer dengan parameter vocabulary yang berisi kata-kata unik
tfidf_matrix = vectorizer.fit_transform(tokenized_documents) # Mengubah kata-kata menjadi vektor dengan metode TF-IDF, atau menghitung bobot dari masing masing kata

query = input("Masukkan query: ")
query_tokens = word_tokenize(query) # Tokenisasi kata atau memecah kalimat menjadi per kata
query_tokens = [word.lower() for word in query_tokens if word.isalpha()]
query_vector = vectorizer.transform([" ".join(query_tokens)]) # Mengubah kata-kata menjadi vektor

cosine_similarities = cosine_similarity(tfidf_matrix, query_vector) # Menghitung cosine similarity antara tfidf_matrix dan query_vector
most_similar_document_index = np.argmax(cosine_similarities) # Mengambil index yang memiliki nilai cosine similarity paling besar
most_similar_document = data_quran[most_similar_document_index] # Mengambil data quran yang memiliki nilai cosine similarity paling besar

print("\nDokumen paling mirip dengan queri:")
print(most_similar_document)

# Jawaban Soal Nomor 3
"""
sorted_indices = np.argsort(cosine_similarities.flatten())[::-1] # Mengurutkan index berdasarkan nilai cosine similarity dari yang terbesar, sebelumnya cosine_similarities di flatten agar menjadi 1 dimensional array
print("\nUrutan Hasil pencarian:")
for index in sorted_indices:
    print(data_quran[index])
"""
    
# Jawaban Soal Nomor 2
"""    
def pre_processing(text):
    pre_process = re.sub('[^a-zA-Z]', ' ', text.lower()) 
    pre_process = re.sub(' +', ' ', pre_process) 
    pre_process = stopwords.remove(pre_process) 
    pre_process = stemmer.stem(pre_process) 
    return pre_process
"""