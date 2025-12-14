# Flowchart Aplikasi Absensi - Kelompok 3

## User Flow - How to Absen (Attendance) - Updated v2

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
