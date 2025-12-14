# Flowchart Aplikasi Absensi - Kelompok 3

## User Flow - How to Absen (Attendance)

```mermaid
flowchart TD
    START([START]) --> OpenApp[Buka Aplikasi Absensi]
    OpenApp --> MainWindow[Tampil Window Aplikasi]
    MainWindow --> Tab1[Pilih Tab: Isi Kehadiran]
    
    Tab1 --> LoadList[Sistem Load Daftar Mahasiswa]
    LoadList --> DisplayList[Tampil List Mahasiswa<br/>Default Status: Alfa]
    
    DisplayList --> Aksi{Pilih Aksi}
    
    Aksi -->|Cari/Filter| Search[Gunakan Search Box &<br/>Sort Dropdown]
    Search --> DisplayList
    
    Aksi -->|Ubah Status| ChangeStatus[Klik Radio Button<br/>Opsi: Alfa, Hadir, Izin, Sakit]
    ChangeStatus --> DisplayList
    
    Aksi -->|Submit| Submit[Klik 'Save/Submit Semua']
    Submit --> SaveDB[Sistem Simpan ke Database]
    SaveDB --> Success[Tampil Success Message]
    Success --> DisplayList
    
    Aksi -->|Kelola Mahasiswa| Tab2[Pindah ke Tab:<br/>Daftar Mahasiswa]
    Tab2 --> ManageList[Tambah/Hapus Mahasiswa]
    ManageList --> DisplayList
    
    Aksi -->|Lihat Laporan| Tab3[Pindah ke Tab:<br/>Rekap Laporan]
    Tab3 --> ViewReport[Lihat & Export Laporan]
    ViewReport --> DisplayList
    
    Aksi -->|Keluar| Close[Klik 'Close App']
    Close --> END([END])
    
    style START fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style END fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style OpenApp fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style MainWindow fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style Tab1 fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style LoadList fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style DisplayList fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style Aksi fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Search fill:#FFC107,stroke:#F57F17,stroke-width:2px,color:#000
    style ChangeStatus fill:#FFC107,stroke:#F57F17,stroke-width:2px,color:#000
    style Submit fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style SaveDB fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style Success fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style Tab2 fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style ManageList fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style Tab3 fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style ViewReport fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style Close fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
```

## Detail Flow: Aksi-Aksi User

### 1. Detail Flow - Cari/Filter Mahasiswa

```mermaid
flowchart TD
    Start([Mulai Cari/Filter]) --> Choose{Pilih Metode}
    
    Choose -->|Search by Name/NIM| SearchBox[Ketik di Search Box]
    SearchBox --> TypeKeyword[Input Keyword:<br/>Nama atau NIM]
    TypeKeyword --> AutoFilter[Sistem Auto Filter<br/>Tampilkan Hasil]
    AutoFilter --> ViewResult[Lihat Hasil Pencarian]
    
    Choose -->|Sort by Field| SortDropdown[Klik Sort Dropdown]
    SortDropdown --> SelectSort{Pilih Urutan}
    SelectSort -->|By NIM| SortNIM[Urutkan Berdasarkan NIM]
    SelectSort -->|By Name| SortName[Urutkan Berdasarkan Nama]
    SelectSort -->|By Status| SortStatus[Urutkan Berdasarkan Status]
    SortNIM --> ApplySort[Sistem Terapkan Sorting]
    SortName --> ApplySort
    SortStatus --> ApplySort
    ApplySort --> ViewResult
    
    ViewResult --> End([Selesai])
    
    style Start fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style End fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style Choose fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style SearchBox fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style TypeKeyword fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style AutoFilter fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style SortDropdown fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style SelectSort fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style SortNIM fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style SortName fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style SortStatus fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style ApplySort fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style ViewResult fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
```

### 2. Detail Flow - Ubah Status Kehadiran

```mermaid
flowchart TD
    Start([Mulai Ubah Status]) --> SelectMhs[Pilih Mahasiswa<br/>dari List]
    SelectMhs --> ViewCurrent[Lihat Status Saat Ini]
    ViewCurrent --> ClickRadio[Klik Radio Button<br/>Status Baru]
    
    ClickRadio --> ChooseStatus{Pilih Status}
    ChooseStatus -->|Option 1| Alfa[Pilih: Alfa]
    ChooseStatus -->|Option 2| Hadir[Pilih: Hadir]
    ChooseStatus -->|Option 3| Izin[Pilih: Izin]
    ChooseStatus -->|Option 4| Sakit[Pilih: Sakit]
    
    Alfa --> UpdateDisplay[Status Berubah di List<br/>Belum Tersimpan]
    Hadir --> UpdateDisplay
    Izin --> UpdateDisplay
    Sakit --> UpdateDisplay
    
    UpdateDisplay --> More{Ubah Mahasiswa Lain?}
    More -->|Ya| SelectMhs
    More -->|Tidak| End([Selesai])
    
    style Start fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style End fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style SelectMhs fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style ViewCurrent fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style ClickRadio fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style ChooseStatus fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Alfa fill:#FFC107,stroke:#F57F17,stroke-width:2px,color:#000
    style Hadir fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style Izin fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style Sakit fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style UpdateDisplay fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style More fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
```

### 3. Detail Flow - Submit/Save Kehadiran

```mermaid
flowchart TD
    Start([Mulai Submit]) --> Review[Review Semua Status<br/>yang Sudah Diubah]
    Review --> ClickSave[Klik Tombol<br/>'Save/Submit Semua']
    ClickSave --> Confirm{Yakin Menyimpan?}
    
    Confirm -->|Tidak| Cancel[Batalkan Submit]
    Cancel --> End([Selesai])
    
    Confirm -->|Ya| Process[Sistem Proses Data]
    Process --> Validate[Validasi Data]
    
    Validate --> ValidCheck{Data Valid?}
    ValidCheck -->|Tidak| ShowError[Tampil Error Message:<br/>Data Tidak Valid]
    ShowError --> End
    
    ValidCheck -->|Ya| SaveDB[Simpan ke Database]
    SaveDB --> DBCheck{Berhasil Disimpan?}
    
    DBCheck -->|Gagal| ShowDBError[Tampil Error Message:<br/>Gagal Menyimpan]
    ShowDBError --> End
    
    DBCheck -->|Sukses| ShowSuccess[Tampil Success Message:<br/>Data Tersimpan]
    ShowSuccess --> RefreshList[Refresh Daftar Mahasiswa]
    RefreshList --> End
    
    style Start fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style End fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style Review fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style ClickSave fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style Confirm fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Cancel fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style Process fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style Validate fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style ValidCheck fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style ShowError fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style SaveDB fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style DBCheck fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style ShowDBError fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style ShowSuccess fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style RefreshList fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
```

### 4. Detail Flow - Kelola Mahasiswa

```mermaid
flowchart TD
    Start([Mulai Kelola Mahasiswa]) --> ClickTab[Klik Tab:<br/>Daftar Mahasiswa]
    ClickTab --> ViewTab[Tampil Form Kelola Mahasiswa]
    ViewTab --> Choose{Pilih Aksi}
    
    Choose -->|Tambah| AddForm[Isi Form Tambah Mahasiswa]
    AddForm --> InputNIM[Input NIM]
    InputNIM --> InputNama[Input Nama]
    InputNama --> InputJurusan[Input Jurusan]
    InputJurusan --> ClickAdd[Klik 'Tambah']
    ClickAdd --> ValidateAdd{Data Valid?}
    ValidateAdd -->|Tidak| ShowAddError[Tampil Error:<br/>Data Tidak Lengkap]
    ShowAddError --> AddForm
    ValidateAdd -->|Ya| SaveAdd[Simpan ke Database]
    SaveAdd --> SuccessAdd[Tampil Success:<br/>Mahasiswa Ditambahkan]
    SuccessAdd --> RefreshTable[Refresh Tabel Mahasiswa]
    
    Choose -->|Hapus| SelectMhs[Pilih Mahasiswa dari Tabel]
    SelectMhs --> ClickDelete[Klik 'Hapus']
    ClickDelete --> ConfirmDelete{Yakin Menghapus?}
    ConfirmDelete -->|Tidak| RefreshTable
    ConfirmDelete -->|Ya| DeleteDB[Hapus dari Database]
    DeleteDB --> SuccessDelete[Tampil Success:<br/>Mahasiswa Dihapus]
    SuccessDelete --> RefreshTable
    
    RefreshTable --> More{Kelola Lagi?}
    More -->|Ya| Choose
    More -->|Tidak| BackTab[Kembali ke Tab:<br/>Isi Kehadiran]
    BackTab --> End([Selesai])
    
    style Start fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style End fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style ClickTab fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style ViewTab fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style Choose fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style AddForm fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style InputNIM fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style InputNama fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style InputJurusan fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style ClickAdd fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style ValidateAdd fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style ShowAddError fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style SaveAdd fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style SuccessAdd fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style SelectMhs fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style ClickDelete fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style ConfirmDelete fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style DeleteDB fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style SuccessDelete fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style RefreshTable fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style More fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style BackTab fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
```

### 5. Detail Flow - Lihat Laporan

```mermaid
flowchart TD
    Start([Mulai Lihat Laporan]) --> ClickTab[Klik Tab:<br/>Rekap Laporan]
    ClickTab --> LoadData[Sistem Load Data Absensi]
    LoadData --> DisplayReport[Tampil Tabel Laporan<br/>Kehadiran]
    
    DisplayReport --> Choose{Pilih Aksi}
    
    Choose -->|Filter by Date| SelectDate[Pilih Tanggal di DatePicker]
    SelectDate --> ApplyDateFilter[Sistem Filter by Tanggal]
    ApplyDateFilter --> UpdateReport[Update Tampilan Laporan]
    UpdateReport --> DisplayReport
    
    Choose -->|Filter by Status| SelectStatus[Pilih Status dari Dropdown]
    SelectStatus --> ApplyStatusFilter[Sistem Filter by Status]
    ApplyStatusFilter --> UpdateReport
    
    Choose -->|View Statistics| ViewStats[Lihat Statistik:<br/>Total Hadir, Alfa, Izin, Sakit]
    ViewStats --> DisplayReport
    
    Choose -->|Export| ClickExport[Klik 'Export ke CSV']
    ClickExport --> ChooseLocation[Pilih Lokasi Simpan File]
    ChooseLocation --> SaveFile[Sistem Simpan File CSV]
    SaveFile --> ExportCheck{Berhasil Export?}
    ExportCheck -->|Gagal| ShowExportError[Tampil Error Message]
    ShowExportError --> DisplayReport
    ExportCheck -->|Sukses| ShowExportSuccess[Tampil Success:<br/>File Tersimpan]
    ShowExportSuccess --> OpenFile{Buka File?}
    OpenFile -->|Ya| OpenCSV[Buka CSV di Excel/App]
    OpenFile -->|Tidak| DisplayReport
    OpenCSV --> DisplayReport
    
    Choose -->|Kembali| BackTab[Kembali ke Tab:<br/>Isi Kehadiran]
    BackTab --> End([Selesai])
    
    style Start fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style End fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style ClickTab fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style LoadData fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style DisplayReport fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style Choose fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style SelectDate fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style ApplyDateFilter fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style UpdateReport fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style SelectStatus fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style ApplyStatusFilter fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style ViewStats fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style ClickExport fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style ChooseLocation fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style SaveFile fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style ExportCheck fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style ShowExportError fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style ShowExportSuccess fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style OpenFile fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style OpenCSV fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style BackTab fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
```

### 6. Detail Flow - Keluar Aplikasi

```mermaid
flowchart TD
    Start([Mulai Keluar]) --> SaveCheck{Ada Perubahan<br/>Belum Tersimpan?}
    
    SaveCheck -->|Ya| WarningMsg[Tampil Warning Message:<br/>Data Belum Tersimpan]
    WarningMsg --> ConfirmSave{Simpan Dulu?}
    ConfirmSave -->|Ya| SaveFirst[Proses Save Data]
    SaveFirst --> SaveResult{Berhasil<br/>Disimpan?}
    SaveResult -->|Tidak| ShowSaveError[Tampil Error Message]
    ShowSaveError --> StillClose{Tetap Keluar?}
    StillClose -->|Tidak| Cancel[Batalkan Keluar]
    Cancel --> End1([Kembali ke Aplikasi])
    StillClose -->|Ya| CloseApp
    SaveResult -->|Ya| CloseApp[Close Aplikasi]
    ConfirmSave -->|Tidak| CloseApp
    
    SaveCheck -->|Tidak| ClickClose[Klik Tombol Close/Exit]
    ClickClose --> ConfirmClose{Yakin Keluar?}
    ConfirmClose -->|Tidak| Cancel
    ConfirmClose -->|Ya| CloseApp
    
    CloseApp --> CleanUp[Cleanup Resources:<br/>Close DB Connection]
    CleanUp --> ExitApp[Exit Aplikasi]
    ExitApp --> End2([END])
    
    style Start fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style End1 fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style End2 fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style SaveCheck fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style WarningMsg fill:#FFC107,stroke:#F57F17,stroke-width:2px,color:#000
    style ConfirmSave fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style SaveFirst fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style SaveResult fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style ShowSaveError fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style StillClose fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Cancel fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style ClickClose fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style ConfirmClose fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style CloseApp fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style CleanUp fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style ExitApp fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
```

## Database Schema Diagram

```mermaid
erDiagram
    MAHASISWA ||--o{ ABSENSI : has
    MAHASISWA {
        string nim PK
        string nama
    }
    ABSENSI {
        int id PK
        string nim FK
        date tanggal
        string keterangan
    }
```

## Module Architecture Diagram

```mermaid
flowchart TB
    Main[main.py] --> GUI[gui.py]
    GUI --> Services[services.py]
    Services --> Queries[queries.py]
    Queries --> DB[(database.py)]
    
    style Main fill:#4CAF50,color:#fff
    style GUI fill:#2196F3,color:#fff
    style Services fill:#FF9800,color:#fff
    style Queries fill:#9C27B0,color:#fff
    style DB fill:#F44336,color:#fff
```

## Class Structure Diagram

```mermaid
classDiagram
    class Database {
        +get_connection()
        +init_db()
    }
    
    class Queries {
        +insert()
        +get_all()
        +search()
    }
    
    class Services {
        +submit_absensi()
        +get_records()
    }
    
    class GUI {
        +setup_tabs()
        +proses_absen()
        +load_laporan()
    }
    
    GUI --> Services
    Services --> Queries
    Queries --> Database
```

## Sequence Diagram - Submit Absensi

```mermaid
sequenceDiagram
    participant User
    participant GUI
    participant Service
    participant DB
    
    User->>GUI: Input NIM & Status
    User->>GUI: Click Submit
    GUI->>Service: submit_absensi()
    Service->>DB: Check & Insert Data
    DB-->>Service: Return Result
    Service-->>GUI: Status Message
    GUI-->>User: Show Result
```

## Data Flow Diagram

```mermaid
flowchart LR
    User[User Input] --> GUI[GUI Layer]
    GUI --> Service[Service Layer]
    Service --> Query[Query Layer]
    Query --> DB[(SQLite Database)]
    
    DB --> Query
    Query --> Service
    Service --> GUI
    GUI --> Display[Display to User]
    
    style User fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style GUI fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style Service fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Query fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style DB fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style Display fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
```
