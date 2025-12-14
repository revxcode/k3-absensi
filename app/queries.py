# SQL Queries module for database operations
from typing import List, Tuple, Optional
from app.database import Database


class MahasiswaQueries:
    # Database queries for Mahasiswa table
    @staticmethod
    def insert_mahasiswa(nim: str, nama: str, jurusan: str) -> bool:
        # Insert new mahasiswa record, returns True if successful, False if NIM already exists
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
        # Get mahasiswa data by NIM
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nama FROM mahasiswa WHERE nim=?", (nim,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def list_mahasiswa(
        keyword: Optional[str] = None, order_by: str = "nim", order_dir: str = "ASC"
    ) -> List[Tuple]:
        # List mahasiswa with optional search and sorting
        # Allowed order_by: nim, nama, jurusan; order_dir: ASC/DESC
        allowed_cols = {"nim", "nama", "jurusan"}
        allowed_dir = {"ASC", "DESC"}
        col = order_by if order_by in allowed_cols else "nim"
        dir_ = order_dir if order_dir in allowed_dir else "ASC"

        conn = Database.get_connection()
        cursor = conn.cursor()
        base = "SELECT nim, nama, jurusan FROM mahasiswa"
        params: Tuple = ()
        if keyword:
            base += " WHERE nama LIKE ? OR nim LIKE ?"
            like = f"%{keyword}%"
            params = (like, like)
        base += f" ORDER BY {col} {dir_}"
        cursor.execute(base, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete_mahasiswa(nim: str) -> bool:
        # Delete mahasiswa and their absensi records
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM absensi WHERE nim=?", (nim,))
            cursor.execute("DELETE FROM mahasiswa WHERE nim=?", (nim,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


class AbsensiQueries:
    # Database queries for Absensi table
    @staticmethod
    def insert_absensi(nim: str, tanggal: str, waktu: str, keterangan: str) -> None:
        # Insert new absensi record
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
        # Check if student already has absensi record for the date
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
        # Get all absensi records with student names
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
        # Search absensi records by name or NIM
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

    @staticmethod
    def update_absensi_status(
        nim: str, tanggal: str, keterangan: str, waktu: str
    ) -> None:
        # Update existing absensi record for a date
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE absensi SET keterangan=?, waktu=? WHERE nim=? AND tanggal=?",
            (keterangan, waktu, nim, tanggal),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def upsert_absensi(nim: str, tanggal: str, waktu: str, keterangan: str) -> None:
        # Insert or update absensi for a given student and date
        if AbsensiQueries.check_existing_absensi(nim, tanggal):
            AbsensiQueries.update_absensi_status(nim, tanggal, keterangan, waktu)
        else:
            AbsensiQueries.insert_absensi(nim, tanggal, waktu, keterangan)
