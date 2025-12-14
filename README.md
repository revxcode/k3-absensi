# Aplikasi Absensi - Kelompok 3

Aplikasi desktop untuk manajemen absensi mahasiswa dengan antarmuka modern menggunakan CustomTkinter, database SQLite, dan fitur-fitur canggih seperti realtime search, sorting, export CSV, dan visual status highlighting.

## Fitur Utama

### 📝 Tab: Isi Kehadiran
- **Daftar mahasiswa** dengan default status Alfa
- **Realtime search** dengan debounce (cari by nama/NIM otomatis tanpa tombol)
- **Sorting** berdasarkan NIM, Nama, atau Status (ASC/DESC)
- **Status radio button** dengan highlight warna:
  - **Alfa** (merah): Absen
  - **Hadir** (hijau): Hadir
  - **Izin** (teal): Izin
  - **Sakit** (orange): Sakit
- **Visual feedback**: Row background berubah warna sesuai status yang dipilih
- **Save/Submit**: Simpan semua status ke database
- **Konfirmasi keluar**: Muncul warning jika ada perubahan belum tersimpan

### 👥 Tab: Daftar Mahasiswa
- **Tambah mahasiswa baru**: Form input NIM, Nama, Jurusan
- **Hapus mahasiswa**: Dengan konfirmasi double-check (ketik ulang NIM)
- **Feedback**: Success/error messages setelah operasi
- **Auto-refresh**: Daftar di Tab 1 otomatis update

### 📊 Tab: Rekap Laporan
- **Realtime search**: Cari by nama/NIM otomatis tanpa tombol
- **Filter tanggal**: Pilih "Hari ini" atau "Semua" untuk menyaring data
- **Sortable columns**: Klik header untuk sort A-Z (Tanggal, Jam, NIM, Nama, Keterangan)
- **Export CSV**: Download laporan sebagai file Excel-compatible
- **Tabel interaktif**: Scrollable dengan styling modern

### 🎨 UI/UX Modern
- CustomTkinter dengan dark theme
- Color-coded status untuk quick scanning
- Console logging untuk FE/BE interactions (debug friendly)
- Responsive layout
- Minimal emoji styling (professional look)

## Struktur Proyek

```
absensi-kelompok-3/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Entry point aplikasi
│   ├── database.py           # Database connection & initialization
│   ├── models.py             # Data models (dataclasses)
│   ├── queries.py            # SQL queries untuk operasi database
│   ├── services.py           # Business logic layer
│   ├── gui.py                # GUI modern (CustomTkinter)
│   └── database/
│       └── schema.sql        # Database schema
├── requirements.txt          # Dependencies
├── README.md                 # Dokumentasi ini
├── flowchart.md              # Diagram aplikasi (User Flow, Arch, Sequence, dll)
└── MODERN_UI_SETUP.md        # Setup guide untuk CustomTkinter
```

## Deskripsi Modul

### 1. **database.py**
Mengelola koneksi database SQLite dan inisialisasi tabel.
- `Database.get_connection()`: Buat koneksi ke SQLite
- `Database.init_db()`: Inisialisasi schema (tabel mahasiswa & absensi)

### 2. **models.py**
Data models menggunakan Python dataclasses:
- `Mahasiswa`: NIM, nama, jurusan
- `Absensi`: id, NIM, tanggal, waktu, keterangan

### 3. **queries.py**
Lapisan data access dengan SQL query terorganisir:
- `MahasiswaQueries`:
  - `insert_mahasiswa()`: Tambah mahasiswa baru
  - `get_all_mahasiswa()`: Ambil semua mahasiswa (with sorting)
  - `get_mahasiswa_by_nim()`: Cari by NIM
  - `delete_mahasiswa()`: Hapus mahasiswa
- `AbsensiQueries`:
  - `insert_absensi()`: Tambah record absensi
  - `check_existing_absensi()`: Validasi duplicate
  - `get_all_absensi()`: Ambil semua records
  - `search_absensi()`: Cari by keyword

### 4. **services.py**
Business logic layer (separation of concerns):
- `MahasiswaService`:
  - `register_mahasiswa()`: Register dengan validasi
  - `list_mahasiswa()`: Get list dengan sorting/filter
  - `delete_mahasiswa()`: Delete dengan validasi
- `AbsensiService`:
  - `apply_statuses_for_today()`: Batch insert status harian
  - `get_all_records()`: Get laporan lengkap
  - `search_records()`: Search records

### 5. **gui.py**
Interface CustomTkinter dengan 3 tabs dan fitur advanced:
- `AplikasiAbsensiModern`:
  - Modern dark theme styling
  - Unsaved changes tracking
  - Realtime debounced search (300ms)
  - Dynamic row highlighting berdasarkan status
  - Sortable table
  - Date filtering
  - CSV export

### 6. **main.py**
Entry point yang clean:
- Inisialisasi database
- Launch GUI

## Cara Menjalankan

### Prasyarat
- Python 3.8+
- pip

### Setup & Run

```bash
# Clone/navigate ke project directory
cd absensi-kelompok-3

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python -m app.main
```

## Dependencies

```
customtkinter>=5.0.0
tkinter (built-in)
sqlite3 (built-in)
```

Lihat `requirements.txt` untuk detail lengkap.

## Alur Penggunaan

1. **Buka Aplikasi**: Jalankan `python -m app.main`
2. **Tab 1 - Isi Kehadiran**:
   - Cari mahasiswa (realtime typing)
   - Ubah status dengan radio button (lihat row berubah warna)
   - Pilih beberapa mahasiswa atau semua
   - Klik "Save" untuk simpan ke database
   - Konsol menampilkan: `[FE] Submit...` lalu `[BE] Tersimpan N baris`
3. **Tab 2 - Daftar Mahasiswa**:
   - Tambah mahasiswa baru dengan NIM, Nama, Jurusan
   - Atau hapus mahasiswa (konfirmasi double-check)
4. **Tab 3 - Rekap Laporan**:
   - Lihat semua record absensi
   - Cari by nama/NIM (realtime)
   - Filter "Hari ini" vs "Semua"
   - Klik header untuk sort
   - Export CSV untuk dibuka di Excel
5. **Keluar**: Klik "Close App" atau X window
   - Jika ada perubahan belum disimpan, muncul konfirmasi

## Console Logging

Aplikasi prints FE/BE interactions untuk debugging:
- `[FE] Reload daftar mahasiswa...` (saat filter/search)
- `[FE] Submit semua status...` (saat save)
- `[BE] Tersimpan N baris status...` (hasil backend)
- `[FE] Refresh laporan...` (saat filter laporan)
- `[BE] Ambil N baris laporan` (fetch result)
- `[BE] Export CSV sukses -> /path/file.csv`

## Keuntungan Struktur Ini

1. **Separation of Concerns**: Setiap modul punya responsibility jelas
2. **Maintainability**: Mudah update/debug per layer
3. **Testability**: Layer terisolasi, bisa di-test independently
4. **Scalability**: Mudah tambah fitur baru tanpa breaking existing
5. **User Experience**: Modern UI dengan responsive interactions
6. **Developer Experience**: Console logs, clear code, modular design

## Pengembangan Lebih Lanjut

Ide untuk upgrade:
- Multi-session support (pagi/siang/malam)
- User authentication (admin login)
- Database migrations
- Unit tests
- Export PDF/Excel dengan template
- Statistik kehadiran (pie chart, report)
- API REST untuk mobile integration
