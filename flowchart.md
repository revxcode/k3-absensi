# Flowchart Aplikasi Absensi - Kelompok 3

## User Flow Diagram

```mermaid
flowchart TD
    Start([User Opens Application]) --> InitDB[System: Initialize Database]
    InitDB --> CreateTables[System: Create Tables if Not Exist]
    CreateTables --> LoadGUI[System: Load GUI Interface]
    LoadGUI --> LoadData[System: Auto-Load Rekap Data]
    LoadData --> ShowMainWindow[Display Main Window with 3 Tabs]
    
    ShowMainWindow --> UserChoice{User Chooses Action}
    
    %% TAB 1: ISI KEHADIRAN
    UserChoice -->|Click Tab 1| Tab1Display[Show: Isi Kehadiran Form]
    Tab1Display --> User1Input[User: Enter NIM in Input Field]
    User1Input --> User1Select[User: Select Status from Dropdown]
    User1Select --> User1Action{User Action}
    User1Action -->|Click Submit| ProcessAbsen[System: Process Absensi]
    ProcessAbsen --> ValidateNIM{Validate: NIM Exists?}
    
    ValidateNIM -->|No| ShowError1[Show Error Dialog:<br/>NIM belum terdaftar]
    ShowError1 --> UpdateLabel1[Update Status Label: Red]
    UpdateLabel1 --> UserChoice
    
    ValidateNIM -->|Yes| CheckDuplicate1{Check: Already Absent Today?}
    CheckDuplicate1 -->|Yes| ShowInfo1[Show Info Dialog:<br/>Sudah absen hari ini]
    ShowInfo1 --> UpdateLabel2[Update Status Label: Orange]
    UpdateLabel2 --> UserChoice
    
    CheckDuplicate1 -->|No| SaveAbsen[System: Save to Database]
    SaveAbsen --> ShowSuccess1[Show Success Dialog]
    ShowSuccess1 --> UpdateLabel3[Update Status Label: Green]
    UpdateLabel3 --> ClearInput1[System: Clear NIM Input]
    ClearInput1 --> AutoRefresh[System: Auto-Refresh Rekap Table]
    AutoRefresh --> UserChoice
    
    User1Action -->|Switch Tab| UserChoice
    
    %% TAB 2: DAFTAR MAHASISWA
    UserChoice -->|Click Tab 2| Tab2Display[Show: Registration Form]
    Tab2Display --> User2Input[User: Fill Form<br/>NIM, Nama, Jurusan]
    User2Input --> User2Action{User Action}
    User2Action -->|Click Simpan| ValidateForm{Validate: NIM & Nama Filled?}
    
    ValidateForm -->|No| ShowWarning[Show Warning Dialog:<br/>NIM dan Nama harus diisi]
    ShowWarning --> UserChoice
    
    ValidateForm -->|Yes| CheckDuplicate2{Check: NIM Already Exists?}
    CheckDuplicate2 -->|Yes| ShowError2[Show Error Dialog:<br/>NIM sudah terdaftar]
    ShowError2 --> UserChoice
    
    CheckDuplicate2 -->|No| SaveMhs[System: Save to Database]
    SaveMhs --> ShowSuccess2[Show Success Dialog:<br/>Data berhasil disimpan]
    ShowSuccess2 --> ClearForm[System: Clear All Form Fields]
    ClearForm --> UserChoice
    
    User2Action -->|Switch Tab| UserChoice
    
    %% TAB 3: REKAP LAPORAN
    UserChoice -->|Click Tab 3| Tab3Display[Show: Rekap Laporan Table]
    Tab3Display --> DisplayAllData[Display All Absensi Records]
    DisplayAllData --> User3Action{User Action}
    
    User3Action -->|Enter Keyword & Click Cari| GetKeyword[System: Get Search Keyword]
    GetKeyword --> SearchProcess[System: Search by Nama/NIM]
    SearchProcess --> ClearTable1[System: Clear Table]
    ClearTable1 --> ShowFiltered[System: Display Filtered Results]
    ShowFiltered --> User3Action
    
    User3Action -->|Click Refresh| ReloadData[System: Reload All Records]
    ReloadData --> ClearTable2[System: Clear Table]
    ClearTable2 --> RedisplayAll[System: Display All Records]
    RedisplayAll --> User3Action
    
    User3Action -->|Click Export CSV| CheckDataAvail{Check: Data Available?}
    CheckDataAvail -->|No| ShowWarning2[Show Warning Dialog:<br/>Tidak ada data]
    ShowWarning2 --> User3Action
    
    CheckDataAvail -->|Yes| OpenDialog[System: Open Save File Dialog]
    OpenDialog --> User3SelectPath{User Selects File Path?}
    User3SelectPath -->|Cancel| User3Action
    User3SelectPath -->|Select| WriteCSV[System: Write Data to CSV]
    WriteCSV --> ShowSuccess3[Show Success Dialog:<br/>Data berhasil diexport]
    ShowSuccess3 --> User3Action
    
    User3Action -->|Switch Tab| UserChoice
    
    UserChoice -->|Close Window| End([Application Closed])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style ShowError1 fill:#FFE4E1
    style ShowError2 fill:#FFE4E1
    style ShowInfo1 fill:#FFE4B5
    style ShowWarning fill:#FFE4B5
    style ShowWarning2 fill:#FFE4B5
    style ShowSuccess1 fill:#E1FFE1
    style ShowSuccess2 fill:#E1FFE1
    style ShowSuccess3 fill:#E1FFE1
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
