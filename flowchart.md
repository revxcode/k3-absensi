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
