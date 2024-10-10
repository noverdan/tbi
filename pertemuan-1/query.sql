CREATE TABLE dosen_pa (
    id char(10) PRIMARY KEY NOT NULL,
    nama varchar(50) NOT NULL
);

CREATE TABLE prodi (
  id varchar(5) PRIMARY KEY NOT NULL,
  nama varchar(50) NOT NULL
);

CREATE TABLE mahasiswa (
  nim varchar(10) PRIMARY KEY NOT NULL,
  nama varchar(50) NOT NULL,
  id_prodi varchar(5) NOT NULL,
  id_dosen_pa char(10) NOT NULL,
  FOREIGN KEY (id_prodi) REFERENCES prodi(id),
  FOREIGN KEY (id_dosen_pa) REFERENCES dosen_pa(id)
);


INSERT INTO dosen_pa (id, nama) VALUES
('0615128401', 'Fandy Setyo Utomo'),
('0617078601', 'Budi Rahardjo'),
('0618038201', 'Sanusi'),
('0623069001', 'Fitrah Rantika'),
('0630119201', 'Rina Andriani');

INSERT INTO prodi (id, nama) VALUES
('BD', 'Bisnis Digital'),
('IF', 'Informatika'),
('ILKOM', 'Ilmu Komunikasi'),
('SI', 'Sistem Informasi'),
('TI', 'Teknologi Informasi');

INSERT INTO mahasiswa (nim, nama_mahasiswa, id_prodi, id_dosen_pa) VALUES
('20SA3150', 'Dewi', 'TI', '0630119201'),
('21SA1134', 'Yulian', 'IF', '0615128401'),
('21SA2123', 'Anton', 'SI', '0617078601'),
('22SA1987', 'Bayu', 'IF', '0615128401'),
('22SA2765', 'Ayu', 'SI', '0630119201');


SELECT * FROM mahasiswa;

SELECT mahasiswa.nama AS mahasiswa, dosen_pa.nama AS dosen, prodi.nama AS prodi FROM mahasiswa JOIN dosen_pa ON mahasiswa.id_dosen_pa = dosen_pa.id JOIN prodi ON mahasiswa.id_prodi = prodi.id;