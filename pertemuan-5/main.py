from connection import DatabaseConnection
import re #regex

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize

db = DatabaseConnection()

query = ("SELECT * FROM id_indonesian limit 50")
data = db.Select(query)

factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()
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


# Tokenization and vocabulary creation
def tokenize_and_create_vocabulary(documents):
    vocabulary = set()
    tokenized_documents = []
    for (index, sura, aya, review) in documents:
        tokens = word_tokenize(review)
        tokens = [word.lower() for word in tokens if word.isalpha()]
        tokenized_documents.append(" ".join(tokens))
        vocabulary.update(tokens)
    return tokenized_documents, list(vocabulary)


# Call tokenize_and_create_vocabulary function
tokenized_docs, vocabulary = tokenize_and_create_vocabulary(corpus)
# Term weighting with Term Frequency - Inverse Document Frequency (TF-IDF)
vectorizer = TfidfVectorizer(vocabulary=vocabulary)
tfidf_matrix = vectorizer.fit_transform(tokenized_docs)
# Tokenization and term weighting for query
query = input('Inputkan Kata Kunci Pencarian: ')
query_tokens = word_tokenize(query)
query_tokens = [word.lower() for word in query_tokens if word.isalpha()]
query_vector = vectorizer.transform([" ".join(query_tokens)])
# Similarity calculation with Cosine Similarity equation
cosine_similarities = cosine_similarity(tfidf_matrix, query_vector)
# Return the document most similar to the user query
most_similar_document_index = np.argmax(cosine_similarities)
most_similar_document = data[most_similar_document_index]
print("\nDokumen paling mirip dengan queri:")
print(most_similar_document)