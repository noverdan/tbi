from main import InvertedIndex

list_mahasiswa = [
    ("21SA1262", "Galang Arsandy Noverdan Putra"),
    ("21SA1122", "Darren Putra"),
    ("22SA1119", "Budi Nugraha Santoso"),
    ("22SA1220", "Diana Siska Putri"),
    ("21SA2311", "Putri Caroline Sirina"),
    ("21SA2231", "Harun Budi Darmawan"),
]

inverted_index = InvertedIndex()
list_mahasiswa_inverted = inverted_index.create_inverted_index(list_mahasiswa)

print("1. Data Awal yang belum di Inverted Index:")
for nim, nama in list_mahasiswa:
    print(f"{nim} = {nama}")
    
print("\n")

print("2. Data setelah di Inverted Index:")
for key, value in list_mahasiswa_inverted.items():
    print(f"{key} = {value}")
    
print("\n")

print("3. Pencarian Data:")
keywords = "Galang Arsandy"
search_result = inverted_index.search(keywords)
print(f"Keyword: {keywords}")
print(f"{len(search_result)} NIM ditemukan dari hasil pencarian '{keywords}': {search_result}")