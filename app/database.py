# Database connection and initialization module
import sqlite3
from typing import Optional
import os


class Database:
    # Database connection manager
    DB_NAME = "absensi_kelompok3.db"
    SCHEMA_FILE = "app/database/schema.sql"

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        # Get database connection
        return sqlite3.connect(Database.DB_NAME)

    @staticmethod
    def init_db() -> None:
        # Initialize database tables if they don't exist
        if not os.path.exists(Database.SCHEMA_FILE):
            print(f"Error: File {Database.SCHEMA_FILE} tidak ditemukan!")
            return

        conn = Database.get_connection()
        cursor = conn.cursor()

        try:
            with open(Database.SCHEMA_FILE, "r") as f:
                sql_script = f.read()

            cursor.executescript(sql_script)
            conn.commit()
            print("Database berhasil diinisialisasi dengan schema.sql")

        except sqlite3.Error as e:
            print(f"Terjadi kesalahan database: {e}")
        finally:
            conn.close()
