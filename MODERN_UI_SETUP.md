# Setup & Run Modern GUI

## Install Dependencies

```bash
# Install CustomTkinter untuk UI modern
pip install customtkinter
```

## Run Application

```bash
# Run aplikasi dengan UI modern
python -m app.main
```

## Features Included (Same as Before)

✅ **Tab 1: Isi Kehadiran**
- List mahasiswa dengan radio buttons (Alfa, Hadir, Izin, Sakit)
- Search by name/NIM
- Sort by NIM, Nama, Status (ASC/DESC)
- Save/Submit semua status sekaligus
- Auto-refresh laporan

✅ **Tab 2: Daftar Mahasiswa**
- Add new mahasiswa
- Delete dengan konfirmasi (re-enter NIM)

✅ **Tab 3: Rekap Laporan**
- View semua absensi records
- Search by name/NIM
- Refresh data
- Export ke CSV

✅ **Global**
- Close App button
- Dark modern theme dengan warna biru
- Responsive layout
- Better UI/UX dengan icons

## What's Different?

- **UI**: Modern dark theme dengan CustomTkinter (bukan plain ttk)
- **Design**: Better spacing, colors, rounded corners, modern buttons
- **Icons**: Added emoji icons untuk better UX
- **Layout**: Improved visual hierarchy dan grouping
- **Functionality**: 100% sama, semua fitur tetap bekerja

## Fallback ke Old GUI

Jika ada masalah, masih bisa gunakan GUI lama:
```python
# Di main.py, ubah:
# from app.gui_modern import AplikasiAbsensiModern
# ke:
# from app.gui import AplikasiAbsensi
```
