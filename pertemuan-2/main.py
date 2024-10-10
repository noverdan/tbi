"""
Membuat indeks terbalik (Inverted Index) dari daftar siswa.
Indeks terbalik adalah struktur data yang digunakan untuk memetakan konten ke lokasinya dalam berkas basis data, atau dalam kasus ini, daftar dictionary.

Indeks ini memungkinkan pencarian teks lengkap yang efisien, 
di mana setiap kata dalam nama siswa dipetakan ke NIM (ID siswa) siswa yang memiliki kata tersebut dalam nama mereka.

sederhananya adalah membalikan indeks, contohnya disini indek nya adalah NIM dan data/value nya adalah nama siswa, 
maka kita akan membaliknya menjadi nama siswa sebagai indek dan NIM sebagai data/value nya. contoh:
21SA1262 = Galang Putra
21SA1122 = Darren Putra
maka hasilnya akan menjadi:
Galang = 21SA1262
Putra = 21SA1262, 21SA1122
Darren = 21SA1122

Yang mana fungsinya inverted indedx adalah untuk mempercepat pencarian data,
karena jika kita ingin mencari data dengan nama Putra, maka kita tidak perlu mencari satu persatu data yang ada.
"""

from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.inverted_index = defaultdict(list)
        
    def create_inverted_index(self, list_mahasiswa):
        for nim, nama in list_mahasiswa:
            for word in nama.split():
                self.inverted_index[word].append(nim)
        return self.inverted_index
    
    def search(self, keywords):
        query_words = keywords.split()
        result = set(self.inverted_index.get(query_words[0], [])) # Mengambil data dari inverted_index berdasarkan kata pertama (index-ke 0/ pertama) dari parameter keywords, Untuk inisiasi
        for word in query_words[1:]:
            result = result.intersection(self.inverted_index.get(word, [])) # Mengambil data dari inverted_index berdasarkan kata kedua dan seterusnya (index-ke 1 dan seterusnya) dari parameter keywords, dan di intersection dengan result sebelumnya (kata pertama dan seterusnya)
        return list(result)


# Hasil Praktikum Lab
if __name__ == '__main__':
    
    list_mahasiswa = [
        ("21SA1262", "Galang Arsandy Noverdan Putra"),
        ("21SA1122", "Darren Putra"),
        ("22SA1119", "Budi Nugraha Santoso"),
        ("22SA1220", "Diana Siska Putri"),
        ("21SA2311", "Putri Caroline Sirina"),
        ("21SA2231", "Harun Budi Darmawan"),
    ]
    inverted_index = InvertedIndex()
    inverted_index.create_inverted_index(list_mahasiswa)
    
    keywords = "Putra"
    search_result = inverted_index.search(keywords)
    print(f"{len(search_result)} NIM ditemukan dari hasil pencarian '{keywords}': {search_result}")


# Tugas di "./tugas_1.py", "./tugas_2.py" dan "./tugas_3.py"