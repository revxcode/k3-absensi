-- schema.sql

-- DROP TABLE IF EXISTS absensi;
-- DROP TABLE IF EXISTS mahasiswa;

-- 1. Tabel Mahasiswa
CREATE TABLE IF NOT EXISTS mahasiswa (
    nim TEXT PRIMARY KEY,
    nama TEXT NOT NULL,
    jurusan TEXT
);

-- 2. Tabel Absensi
CREATE TABLE IF NOT EXISTS absensi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nim TEXT,
    tanggal TEXT,
    waktu TEXT,
    keterangan TEXT,
    FOREIGN KEY (nim) REFERENCES mahasiswa (nim)
);

-- 3. Masukkan Dummy Data
-- Menggunakan INSERT OR IGNORE agar tidak error jika dijalankan 2x
INSERT OR IGNORE INTO mahasiswa (nim, nama, jurusan) VALUES 
('101', 'Ahmad Dani', 'Teknik Informatika'),
('102', 'Budi Santoso', 'Sistem Informasi'),
('103', 'Citra Kirana', 'Teknik Informatika'),
('104', 'Dedi Corbuzier', 'Manajemen Informatika');

-- Dummy Data Absensi (Opsional)
INSERT OR IGNORE INTO absensi (nim, tanggal, waktu, keterangan) VALUES
('101', '2023-10-25', '07:55:00', 'Hadir'),
('102', '2023-10-25', '08:05:00', 'Hadir');