from main import InvertedIndex

list_mahasiswa = [
    ("21SA1262", "Galang Arsandy Noverdan Putra"),
    ("21SA1122", "Darren Putra"),
    ("22SA1119", "Budi Nugraha Santoso"),
    ("22SA1220", "Diana Siska Putri"),
    ("21SA2311", "Putri Caroline Sirina"),
    ("21SA2231", "Harun Budi Darmawan"),
]

class NotCaseSensitive(InvertedIndex):
    def create_inverted_index(self, list_mahasiswa):
        for nim, nama in list_mahasiswa:
            for word in nama.split():
                self.inverted_index[word.lower()].append(nim)
        return self.inverted_index
    
    def search(self, keywords):
        query_words = keywords.lower().split()
        result = set(self.inverted_index.get(query_words[0], [])) 
        for word in query_words[1:]:
            result = result.intersection(self.inverted_index.get(word, [])) 
        return list(result)

if __name__ == '__main__':
    inverted_index = NotCaseSensitive()
    list_mahasiswa_inverted = inverted_index.create_inverted_index(list_mahasiswa)

    keywords = "galang aRsAndY"
    search_result = inverted_index.search(keywords)
    print(f"{len(search_result)} NIM ditemukan dari hasil pencarian '{keywords}': {search_result}")



