import re 
class MyDocument:
    def __init__(self):
        self.index = {} # Membuat dictionary untuk menampung index

    def add_inverted_index_doc(self, doc_id, text):
        tokens = re.findall(r'\b\w+\b', text.lower()) # menemukan kata dan memecah text menjadi per kata
        for token in tokens:
            if token not in self.index:
                self.index[token] = set() # Jika kata belum ada di dalam self.index maka akan dibuatkan set kosong
            self.index[token].add(doc_id) # Menambahkan doc_id ke dalam set di self.index yang sudah dibuat

    def bool_retrieval_search(self,query):
        tokens = re.findall(r'[+-]\w+\b', query.lower()) # Menemukan kata yang diawali dengan simbol + atau -
        tokens = sorted({elem.strip() for elem in tokens}) # Mengurutkan kata(tokens) yang sudah ditemukan 

        results =set() # Membuat set kosong untuk menampung hasil pencarian
        for token in tokens:
            if self.index.get(token[1:]) is not None: # Mengecek apakah kata yang dicari ada di dalam index, token[1:] digunakan untuk menghilangkan simbol + atau -
                if token.startswith('+'): 
                    result_token = token[1:]
                    results = results.union(self.index[result_token]) # Jika token diawali dengan simbol + maka hasil pencarian akan di gabungkan
                elif token.startswith('-'):
                    result_token = token[1:]
                    results = results.difference(self.index[result_token]) # Jika token diawali dengan simbol - maka hasil pencarian akan di kurangkan
        return results
    
    def lihat_index(self):
        return self.index

if __name__ == '__main__':
    document = MyDocument()
    document.add_inverted_index_doc(1, "The quickly brown fox jumps over the lazy dog.")
    document.add_inverted_index_doc(2, "The five boxing wizards jumps quickly.")
    document.add_inverted_index_doc(3, "Pack my box with five dozen liquor jugs.")
    document.add_inverted_index_doc(4, "How quick daft jumping zebras vex.")
    document.add_inverted_index_doc(5, "Two driven jocks help fax my big quiz.")

    print(document.bool_retrieval_search("+Quickly -fox +zebras +ada"))