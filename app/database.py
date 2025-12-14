# Database connection and initialization module
import sqlite3
from typing import Optional


class Database:
    # Database connection manager
    DB_NAME = "absensi_kelompok3.db"

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        # Get database connection
        return sqlite3.connect(Database.DB_NAME)

    @staticmethod
    def init_db() -> None:
        # Initialize database tables if they don't exist
        conn = Database.get_connection()
        cursor = conn.cursor()

        # Tabel Mahasiswa
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mahasiswa (
                nim TEXT PRIMARY KEY,
                nama TEXT NOT NULL,
                jurusan TEXT
            )
            """
        )

        # Tabel Absensi
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS absensi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nim TEXT,
                tanggal TEXT,
                waktu TEXT,
                keterangan TEXT,
                FOREIGN KEY (nim) REFERENCES mahasiswa (nim)
            )
            """
        )

        conn.commit()
        conn.close()
