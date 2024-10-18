import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from connection import DatabaseConnection
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

db = DatabaseConnection()
query = ("SELECT * FROM id_indonesian limit 20")
data = db.Select(query)

#Create stopword remover

stopword = StopWordRemoverFactory().create_stop_word_remover()

#Create stemmer
stemmer = StopWordRemoverFactory().create_stemmer()

#Create an empty list of corpus
corpus = []

for (index, sura, aya, text) in data:
    #[^a-zA-Z]: eliminate number and punctuation, except alphabet a-z and A-Z
    review = re.sub('[^a-zA-Z]', ' ', text)

    #Lowercase operation
    review = review.lower()


    #Stopwords removal operation
    review = stopword.remove(review)
    jumlah_kata_awal = len(review.split())
    kondisi = True

    # print(index, ": ", review)

    while (kondisi):
        review = re.sub(' +', ' ', review)
        review = stopword.remove(review)
        jumlah_kata_baru = len(review.split())

        if (jumlah_kata_awal == jumlah_kata_baru):
            kondisi = False
        else:
            jumlah_kata_awal = jumlah_kata_baru

            #Stemming operation
            review = stemmer.stem(review)

            #Add data quran verses to List
            corpus.append((index, sura, aya, review))

        # print(index, ": ", review)

class InvertedIndex:
    def __init__(self):
        self.indek = {}
    def add_document(self, doc_id, content):
        tokens = re.findall(r'\b\w+\b', content.lower())
        # print(tokens)
        for token in tokens:
            if token not in self.indek:
                self.indek[token] = set()
            self.indek[token].add(doc_id)
        return self.indek

indeks = InvertedIndex()
print(corpus)

for (index, sura, aya, review) in corpus:
    # print(review)
    # print("=============================================")

    inde = indeks.add_document(index, review)
    # print(inde)