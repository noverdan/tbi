'''
Create class 'DatabaseConnection' to handle query operation and 
connection between python and MySQL database.
'''
import mysql.connector
from mysql.connector import errorcode

config = {
	'user' : 'root',
	'database' : 'quran' 
}

class DatabaseConnection():
    
    #Constructor
    def __init__(self):
        
        try:
            #Create database connection
            self.db_connect = mysql.connector.connect(**config)
            
            #Create a Cursor
            self.cursor = self.db_connect.cursor()
            
        except mysql.connector.Error as err:
            
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
    
    def Select(self, query):
        
        self.cursor.execute(query)
        self.data = self.cursor.fetchall()
        return self.data
    
    #Destructor
    def __del__(self):
        
        #Close Cursor
        self.cursor.close()
        
        #Close DB Connection
        self.db_connect.close()
#==========================================================================End

'''
Ambil data nomor index, surat, ayat, dan teks ayat dari tabel id_indonesian
'''
db = DatabaseConnection()

query = ("SELECT * FROM id_indonesian limit 100")

data = db.Select(query)
#==========================================================================End

'''
Perform text pre-processing: punctuation removal, lowercase operation, 
stopwords removal, and stemming operation
'''
#Regular expression operations: https://docs.python.org/3/library/re.html
import re

#Dokumentasi Sastrawi Stemmer: https://pypi.org/project/Sastrawi/
#import StopWordRemoverFactory class
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

#Create stemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

#Create an empty list of corpus
corpus = []

for (index, sura, aya, text) in data:
    # [^a-zA-Z] means: eliminate number and punctuation, except alphabet a-z and A-Z
    review = re.sub('[^a-zA-Z]', ' ', text)
    
    #Lowercase operation
    review = review.lower()
    
    #Stopwords removal operation
    review = stopword.remove(review)
    jumlah_kata_awal = len(review.split())
    kondisi = True
    while(kondisi):
        review = re.sub(' +', ' ', review)
        review = stopword.remove(review)
        
        jumlah_kata_baru = len(review.split())
        if(jumlah_kata_awal == jumlah_kata_baru):
            kondisi = False
        else:
            jumlah_kata_awal = jumlah_kata_baru
    
    #Stemming operation
    review = stemmer.stem(review)
    
    #Add data quran verses to List
    corpus.append((index, sura, aya, review))
#==========================================================================End

# https://radimrehurek.com/gensim/index.html
from gensim import corpora, models, similarities


# Pra-pemrosesan teks
tokenized_documents = [doc.split() for (index, sura, aya, doc) in corpus]
dictionary = corpora.Dictionary(tokenized_documents)
corpusx = [dictionary.doc2bow(doc) for doc in tokenized_documents]

# Membangun model Latent Semantic Indexing (LSI)
# https://radimrehurek.com/gensim/models/lsimodel.html
lsi = models.LsiModel(corpusx, id2word=dictionary, num_topics=50)

# Soal No 2
def pre_processing(text):
    pre_process = re.sub('[^a-zA-Z]', ' ', text.lower()) # Menghilaangkan karakter selain huruf a-z dan A-Z dan diubah menjadi spasi. Lalu diubah menjadi huruf kecil
    pre_process = re.sub(' +', ' ', pre_process) # Menghilangkan spasi yang berlebihan
    pre_process = stopword.remove(pre_process) # Menghilangkan stopwords atau kata-kata yang tidak penting
    pre_process = stemmer.stem(pre_process) # Melakukan stemming atau mengubah kata-kata menjadi kata dasar
    return pre_process

# Query pencarian
query = input('Inputkan Keywords: ')

# Transformasi query
query_bow = dictionary.doc2bow(pre_processing(query).split())
query_lsi = lsi[query_bow]

# Membangun index similarity
# https://radimrehurek.com/gensim/similarities/docsim.html
index = similarities.MatrixSimilarity(lsi[corpusx])

# Hitung similarity antara query dan dokumen
sims = index[query_lsi]

# Urutkan dokumen berdasarkan similarity
ranked_documents = sorted(enumerate(sims), key=lambda item: -item[1])

# Tampilkan hasil
print("\nHasil Temu Balik Informasi:\n")
for rank, (doc_id, score) in enumerate(ranked_documents):
    print(f"Dokumen {rank + 1}: {data[doc_id]}\n (Similarity: {score:.4f})\n")
    
    if(rank == 2):
        break

