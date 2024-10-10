from db_connection import DatabaseConnection
from pandas import DataFrame
from pandas import ExcelWriter

db = DatabaseConnection()

def export_to_excel(data, filename, col):
    df = DataFrame(data, columns=col)
    writer = ExcelWriter(filename)
    df.to_excel(writer, index=False)
    writer._save()

mahasiswa = db.Select("SELECT * FROM mahasiswa")
bimbingan_mahasiswa = db.Select("SELECT m.nim, m.nama, p.nama, d.nama \
	FROM mahasiswa m \
	JOIN prodi p ON m.id_prodi = p.id \
	JOIN dosen_pa d ON m.id_dosen_pa = d.id"
)
dosen_kosong = db.Select("SELECT d.id, d.nama \
	FROM dosen_pa d \
	LEFT JOIN mahasiswa m ON d.id = m.id_dosen_pa \
	WHERE m.nim IS NULL"
)

export_to_excel(mahasiswa, "./excel/mahasiswa.xlsx", ["NIM", "Nama", "ID Prodi", "ID Dosen PA"])
export_to_excel(bimbingan_mahasiswa, "./excel/bimbingan_mahasiswa.xlsx", ["NIM", "Nama Mahasiswa", "Prodi", "Dosen PA"])
export_to_excel(dosen_kosong, "./excel/dosen_kosong.xlsx", ["ID Dosen PA", "Nama Dosen PA"])