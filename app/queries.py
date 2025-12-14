"""
SQL Queries module for database operations
"""

from typing import List, Tuple, Optional
from app.database import Database


class MahasiswaQueries:
    """Database queries for Mahasiswa table"""

    @staticmethod
    def insert_mahasiswa(nim: str, nama: str, jurusan: str) -> bool:
        """
        Insert new mahasiswa record
        Returns True if successful, False if NIM already exists
        """
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO mahasiswa VALUES (?, ?, ?)", (nim, nama, jurusan)
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def get_mahasiswa_by_nim(nim: str) -> Optional[Tuple]:
        """Get mahasiswa data by NIM"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nama FROM mahasiswa WHERE nim=?", (nim,))
        data = cursor.fetchone()
        conn.close()
        return data


class AbsensiQueries:
    """Database queries for Absensi table"""

    @staticmethod
    def insert_absensi(nim: str, tanggal: str, waktu: str, keterangan: str) -> None:
        """Insert new absensi record"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO absensi (nim, tanggal, waktu, keterangan) VALUES (?, ?, ?, ?)",
            (nim, tanggal, waktu, keterangan),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def check_existing_absensi(nim: str, tanggal: str) -> bool:
        """Check if student already has absensi record for the date"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM absensi WHERE nim=? AND tanggal=?", (nim, tanggal)
        )
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    @staticmethod
    def get_all_absensi() -> List[Tuple]:
        """Get all absensi records with student names"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT absensi.tanggal, absensi.waktu, absensi.nim, 
                   mahasiswa.nama, absensi.keterangan
            FROM absensi
            JOIN mahasiswa ON absensi.nim = mahasiswa.nim
            ORDER BY absensi.id DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def search_absensi(keyword: str) -> List[Tuple]:
        """Search absensi records by name or NIM"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT absensi.tanggal, absensi.waktu, absensi.nim,
                   mahasiswa.nama, absensi.keterangan
            FROM absensi
            JOIN mahasiswa ON absensi.nim = mahasiswa.nim
            WHERE mahasiswa.nama LIKE ? OR absensi.nim LIKE ?
            ORDER BY absensi.id DESC
        """
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        conn.close()
        return rows
