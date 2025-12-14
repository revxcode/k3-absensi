# Flowchart Aplikasi Absensi - Kelompok 3

## User Flow - How to Absen (Attendance)

```mermaid
flowchart TD
    START([START]) --> OpenApp[Buka Aplikasi Absensi]
    OpenApp --> MainWindow[Tampil Window dengan 3 Tab]
    MainWindow --> ClickTab1[Pilih Tab 'Isi Kehadiran']
    ClickTab1 --> InputNIM[Masukkan NIM Mahasiswa]
    InputNIM --> SelectStatus[Pilih Status: Hadir/Izin/Sakit]
    SelectStatus --> ClickSubmit[Klik Tombol 'SUBMIT ABSENSI']
    
    ClickSubmit --> CheckNIM{Apakah NIM<br/>Terdaftar?}
    
    CheckNIM -->|Tidak| ErrorMsg[Tampil Error:<br/>'NIM belum terdaftar']
    ErrorMsg --> TryAgain{Coba Lagi?}
    TryAgain -->|Ya| InputNIM
    TryAgain -->|Tidak| END1([END])
    
    CheckNIM -->|Ya| CheckToday{Sudah Absen<br/>Hari Ini?}
    
    CheckToday -->|Ya| InfoMsg[Tampil Info:<br/>'Sudah absen hari ini']
    InfoMsg --> Done{Selesai?}
    Done -->|Ya| END2([END])
    Done -->|Absen Lagi| InputNIM
    
    CheckToday -->|Tidak| SaveData[Simpan Data Absensi ke Database]
    SaveData --> SuccessMsg[Tampil Success:<br/>'Berhasil absen']
    SuccessMsg --> ClearForm[Form NIM Otomatis Terhapus]
    ClearForm --> NextAction{Mau Absen<br/>Lagi?}
    NextAction -->|Ya| InputNIM
    NextAction -->|Tidak| END3([END])
    
    style START fill:#90EE90
    style END1 fill:#FFB6C1
    style END2 fill:#FFB6C1
    style END3 fill:#FFB6C1
    style ErrorMsg fill:#FFE4E1
    style InfoMsg fill:#FFE4B5
    style SuccessMsg fill:#E1FFE1
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
