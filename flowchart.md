# Flowchart Aplikasi Absensi - Kelompok 3

## User Flow - How to Absen (Attendance) - Updated v2

```mermaid
flowchart TD
    START([START]) --> OpenApp[Buka Aplikasi Absensi]
    OpenApp --> MainWindow[Tampil Window dengan 3 Tab + Close App Button]
    MainWindow --> ClickTab1[Pilih Tab 'Isi Kehadiran']
    ClickTab1 --> LoadList[Sistem: Load Daftar Mahasiswa]
    LoadList --> DisplayList[Tampil List Mahasiswa dengan Status Radio<br/>Default: Alfa]
    
    DisplayList --> UserAction{Aksi Dosen}
    
    %% Search & Filter
    UserAction -->|Cari Nama/NIM| InputSearch[Masukkan Keyword di Search Box]
    InputSearch --> ClickCari[Klik Tombol 'Cari']
    ClickCari --> FilterList[Sistem: Filter List by Nama/NIM]
    FilterList --> DisplayFiltered[Tampil Mahasiswa Hasil Filter]
    DisplayFiltered --> UserAction
    
    %% Sort
    UserAction -->|Ubah Sort| SelectSort[Pilih dari Dropdown:<br/>NIM ASC/DESC<br/>Nama ASC/DESC<br/>Status ASC/DESC]
    SelectSort --> ApplySort[Sistem: Sort List Sesuai Pilihan]
    ApplySort --> DisplaySorted[Tampil List Terurut]
    DisplaySorted --> UserAction
    
    %% Reset Filters
    UserAction -->|Reset| ClickReset[Klik Tombol 'Reset']
    ClickReset --> ClearFilters[Sistem: Clear Search & Sort]
    ClearFilters --> ReloadAll[Reload Semua Mahasiswa]
    ReloadAll --> DisplayList
    
    %% Select Status
    UserAction -->|Pilih Status| SelectRadio[Dosen: Klik Radio Button untuk Setiap Mahasiswa<br/>Opsi: Alfa, Hadir, Izin, Sakit]
    SelectRadio --> StatusSelected[Status Tersimpan di Memory]
    StatusSelected --> CheckMore{Ada Lagi Yang<br/>Perlu Diubah?}
    CheckMore -->|Ya| UserAction
    CheckMore -->|Tidak| SubmitAll[Dosen: Klik 'Save/Submit Semua']
    
    %% Save All
    SubmitAll --> ValidateList{Ada Mahasiswa<br/>di List?}
    ValidateList -->|Tidak| WarnEmpty[Tampil Warning:<br/>'Tidak ada mahasiswa']
    WarnEmpty --> UserAction
    ValidateList -->|Ya| SaveDB[Sistem: Upsert Semua Status ke Database<br/>untuk Tanggal Hari Ini]
    SaveDB --> SuccessAll[Tampil Success:<br/>'Sukses submit X status']
    SuccessAll --> RefreshLaporan[Sistem: Auto-Refresh Tab Rekap Laporan]
    RefreshLaporan --> UserAction
    
    %% Other Tabs or Close
    UserAction -->|Pindah Tab| TabChoice{Pilih Tab}
    TabChoice -->|Daftar Mahasiswa| DaftarTab[Ke Tab Daftar Mahasiswa]
    DaftarTab --> ManageStudent[Tambah/Hapus Mahasiswa]
    ManageStudent --> ClickTab1
    
    TabChoice -->|Rekap Laporan| LaporanTab[Ke Tab Rekap Laporan]
    LaporanTab --> ViewRecap[Lihat Laporan Absensi]
    ViewRecap --> ClickTab1
    
    UserAction -->|Selesai| CloseApp[Klik Tombol 'Close App']
    CloseApp --> ExitApp([END])
    
    style START fill:#90EE90
    style ExitApp fill:#FFB6C1
    style DisplayList fill:#FFE4E1
    style SelectRadio fill:#FFE4E1
    style WarnEmpty fill:#FFE4E1
    style SuccessAll fill:#E1FFE1
    style DisplayFiltered fill:#E1F5FF
    style DisplaySorted fill:#E1F5FF
    style RefreshLaporan fill:#E1FFE1
```

## Database Schema Diagram

```mermaid
erDiagram
    MAHASISWA ||--o{ ABSENSI : has
    MAHASISWA {
        string nim PK
        string nama
        string jurusan
    }
    ABSENSI {
        int id PK
        string nim FK
        string tanggal
        string waktu
        string keterangan
    }
```

## Module Architecture Diagram

```mermaid
flowchart LR
    Main[main.py] --> Database[database.py]
    Main --> GUI[gui.py]
    
    GUI --> Services[services.py]
    Services --> Queries[queries.py]
    Services --> Models[models.py]
    Queries --> Database
    
    subgraph "Presentation Layer"
        GUI
    end
    
    subgraph "Business Logic Layer"
        Services
        Models
    end
    
    subgraph "Data Access Layer"
        Queries
        Database
    end
```

## Class Structure Diagram

```mermaid
classDiagram
    class Database {
        +String DB_NAME
        +get_connection() Connection
        +init_db() void
    }
    
    class MahasiswaQueries {
        +insert_mahasiswa(nim, nama, jurusan) bool
        +get_mahasiswa_by_nim(nim) Tuple
    }
    
    class AbsensiQueries {
        +insert_absensi(nim, tanggal, waktu, keterangan) void
        +check_existing_absensi(nim, tanggal) bool
        +get_all_absensi() List
        +search_absensi(keyword) List
    }
    
    class MahasiswaService {
        +register_mahasiswa(nim, nama, jurusan) bool
    }
    
    class AbsensiService {
        +submit_absensi(nim, keterangan) Tuple
        +get_all_records() List
        +search_records(keyword) List
    }
    
    class AplikasiAbsensi {
        -root: Tk
        -tabs: Notebook
        +setup_tab_absensi() void
        +setup_tab_daftar() void
        +setup_tab_laporan() void
        +proses_absen() void
        +proses_daftar() void
        +proses_cari() void
        +load_laporan() void
        +export_ke_csv() void
    }
    
    MahasiswaQueries --> Database
    AbsensiQueries --> Database
    MahasiswaService --> MahasiswaQueries
    AbsensiService --> AbsensiQueries
    AplikasiAbsensi --> MahasiswaService
    AplikasiAbsensi --> AbsensiService
```

## Sequence Diagram - Submit Absensi

```mermaid
sequenceDiagram
    participant User
    participant GUI as AplikasiAbsensi
    participant Service as AbsensiService
    participant Query as AbsensiQueries
    participant MQ as MahasiswaQueries
    participant DB as Database
    
    User->>GUI: Input NIM & Status
    User->>GUI: Click Submit
    GUI->>Service: submit_absensi(nim, keterangan)
    Service->>MQ: get_mahasiswa_by_nim(nim)
    MQ->>DB: SELECT nama FROM mahasiswa WHERE nim=?
    DB-->>MQ: Return data
    MQ-->>Service: Return (nama)
    
    alt NIM Not Found
        Service-->>GUI: ("NIM_TIDAK_ADA", None)
        GUI-->>User: Show Error Message
    else NIM Found
        Service->>Query: check_existing_absensi(nim, tanggal)
        Query->>DB: SELECT * FROM absensi WHERE nim=? AND tanggal=?
        DB-->>Query: Return result
        Query-->>Service: Return exists
        
        alt Already Absent Today
            Service-->>GUI: ("SUDAH_ABSEN", nama)
            GUI-->>User: Show Info Message
        else Not Yet Absent
            Service->>Query: insert_absensi(nim, tanggal, waktu, keterangan)
            Query->>DB: INSERT INTO absensi VALUES(...)
            DB-->>Query: Success
            Query-->>Service: Success
            Service-->>GUI: ("SUKSES", nama)
            GUI->>GUI: Refresh Table
            GUI-->>User: Show Success Message
        end
    end
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
    
    style User fill:#e1f5ff
    style GUI fill:#fff4e1
    style Service fill:#ffe1f5
    style Query fill:#e1ffe1
    style DB fill:#f5e1ff
    style Display fill:#e1f5ff
```
