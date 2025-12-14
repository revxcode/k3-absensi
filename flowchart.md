# Flowchart Aplikasi Absensi - Kelompok 3

## Application Flow Diagram

```mermaid
flowchart TD
    Start([Start Application]) --> InitDB[Initialize Database]
    InitDB --> CreateTables{Tables Exist?}
    CreateTables -->|No| CreateMahasiswaTable[Create Mahasiswa Table]
    CreateMahasiswaTable --> CreateAbsensiTable[Create Absensi Table]
    CreateAbsensiTable --> LoadGUI[Load GUI]
    CreateTables -->|Yes| LoadGUI
    
    LoadGUI --> MainMenu{Select Tab}
    
    MainMenu -->|Tab 1| IsiKehadiran[Isi Kehadiran]
    MainMenu -->|Tab 2| DaftarMahasiswa[Daftar Mahasiswa Baru]
    MainMenu -->|Tab 3| RekapLaporan[Rekap Laporan]
    
    %% Tab 1: Isi Kehadiran Flow
    IsiKehadiran --> InputNIM[Input NIM]
    InputNIM --> SelectStatus[Select Status: Hadir/Izin/Sakit]
    SelectStatus --> SubmitAbsen[Submit Absensi]
    SubmitAbsen --> CheckNIM{NIM Exists?}
    CheckNIM -->|No| ErrorNIM[Error: NIM Tidak Ditemukan]
    ErrorNIM --> MainMenu
    CheckNIM -->|Yes| CheckTodayAbsen{Already Absent Today?}
    CheckTodayAbsen -->|Yes| InfoSudahAbsen[Info: Sudah Absen Hari Ini]
    InfoSudahAbsen --> MainMenu
    CheckTodayAbsen -->|No| SaveAbsensi[Save Absensi Record]
    SaveAbsensi --> SuccessAbsen[Success: Absensi Tersimpan]
    SuccessAbsen --> RefreshTable[Auto Refresh Table]
    RefreshTable --> MainMenu
    
    %% Tab 2: Daftar Mahasiswa Flow
    DaftarMahasiswa --> InputRegData[Input NIM, Nama, Jurusan]
    InputRegData --> ValidateInput{Data Valid?}
    ValidateInput -->|No| WarningInput[Warning: NIM dan Nama Harus Diisi]
    WarningInput --> MainMenu
    ValidateInput -->|Yes| CheckDuplicate{NIM Already Exists?}
    CheckDuplicate -->|Yes| ErrorDuplicate[Error: NIM Sudah Terdaftar]
    ErrorDuplicate --> MainMenu
    CheckDuplicate -->|No| SaveMahasiswa[Save Mahasiswa Data]
    SaveMahasiswa --> SuccessReg[Success: Data Mahasiswa Tersimpan]
    SuccessReg --> ClearForm[Clear Form]
    ClearForm --> MainMenu
    
    %% Tab 3: Rekap Laporan Flow
    RekapLaporan --> LoadInitial[Load All Records]
    LoadInitial --> DisplayTable[Display in Table]
    DisplayTable --> LaporanMenu{User Action}
    LaporanMenu -->|Search| InputKeyword[Input Search Keyword]
    InputKeyword --> SearchDB[Search in Database]
    SearchDB --> FilterResults[Filter by Nama/NIM]
    FilterResults --> UpdateTable[Update Table with Results]
    UpdateTable --> LaporanMenu
    LaporanMenu -->|Refresh| ReloadAll[Reload All Records]
    ReloadAll --> DisplayTable
    LaporanMenu -->|Export CSV| CheckData{Data Available?}
    CheckData -->|No| WarnEmpty[Warning: Tidak Ada Data]
    WarnEmpty --> LaporanMenu
    CheckData -->|Yes| SelectFile[Select File Location]
    SelectFile --> ExportCSV[Export to CSV]
    ExportCSV --> SuccessExport[Success: Data Exported]
    SuccessExport --> LaporanMenu
    LaporanMenu -->|Back| MainMenu
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
