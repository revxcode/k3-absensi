# Aplikasi Absensi - Kelompok 3

## Struktur Proyek

```
absensi-kelompok-3/
├── app/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # Entry point aplikasi
│   ├── database.py       # Database connection & initialization
│   ├── queries.py        # SQL queries untuk operasi database
│   ├── models.py         # Data models (dataclasses)
│   ├── services.py       # Business logic layer
│   └── gui.py            # GUI (tkinter interface)
├── requirements.txt      # Dependencies
└── README.md            # Dokumentasi
```

## Deskripsi Modul

### 1. **database.py**
Mengelola koneksi database dan inisialisasi tabel.
- `Database.get_connection()`: Membuat koneksi ke database
- `Database.init_db()`: Inisialisasi tabel mahasiswa dan absensi

### 2. **queries.py**
Berisi semua query SQL yang diorganisir dalam class-class:
- `MahasiswaQueries`: Query untuk tabel mahasiswa
  - `insert_mahasiswa()`: Insert mahasiswa baru
  - `get_mahasiswa_by_nim()`: Ambil data mahasiswa by NIM
- `AbsensiQueries`: Query untuk tabel absensi
  - `insert_absensi()`: Insert record absensi
  - `check_existing_absensi()`: Cek apakah sudah absen
  - `get_all_absensi()`: Ambil semua record absensi
  - `search_absensi()`: Cari absensi by keyword

### 3. **models.py**
Data models menggunakan dataclasses:
- `Mahasiswa`: Model data mahasiswa
- `Absensi`: Model data absensi
- `AbsensiRecord`: Model record absensi lengkap dengan info mahasiswa

### 4. **services.py**
Business logic layer yang memisahkan logika bisnis dari database:
- `MahasiswaService`: Service untuk operasi mahasiswa
  - `register_mahasiswa()`: Registrasi mahasiswa baru
- `AbsensiService`: Service untuk operasi absensi
  - `submit_absensi()`: Submit absensi dengan validasi
  - `get_all_records()`: Ambil semua record
  - `search_records()`: Cari record by keyword

### 5. **gui.py**
Interface tkinter yang terpisah dari logic:
- `AplikasiAbsensi`: Main GUI class
  - Tab 1: Isi Kehadiran
  - Tab 2: Daftar Mahasiswa Baru
  - Tab 3: Rekap Laporan (dengan search & export CSV)

### 6. **main.py**
Entry point aplikasi yang simpel dan clean:
- Inisialisasi database
- Jalankan GUI

## Cara Menjalankan

```bash
python -m app.main
```

## Keuntungan Struktur Modular

1. **Separation of Concerns**: Setiap modul punya tanggung jawab yang jelas
2. **Maintainability**: Mudah untuk maintenance dan update
3. **Testability**: Mudah untuk testing setiap komponen
4. **Reusability**: Modul bisa digunakan ulang
5. **Scalability**: Mudah untuk menambah fitur baru
6. **Readability**: Kode lebih mudah dibaca dan dipahami
