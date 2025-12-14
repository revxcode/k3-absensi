"""
Business logic services for the application
"""

from datetime import datetime
from typing import Tuple, List
from app.queries import MahasiswaQueries, AbsensiQueries


class MahasiswaService:
    """Service layer for Mahasiswa operations"""

    @staticmethod
    def register_mahasiswa(nim: str, nama: str, jurusan: str) -> bool:
        """
        Register a new mahasiswa
        Returns True if successful, False if NIM already exists
        """
        return MahasiswaQueries.insert_mahasiswa(nim, nama, jurusan)


class AbsensiService:
    """Service layer for Absensi operations"""

    @staticmethod
    def submit_absensi(nim: str, keterangan: str) -> Tuple[str, str]:
        """
        Submit absensi for a student
        Returns: (status, nama) where status can be:
            - "SUKSES": Successfully recorded
            - "SUDAH_ABSEN": Already has absensi for today
            - "NIM_TIDAK_ADA": NIM not found in database
        """
        # Check if NIM exists
        data = MahasiswaQueries.get_mahasiswa_by_nim(nim)

        if data:
            nama = data[0]
            now = datetime.now()
            tanggal = now.strftime("%Y-%m-%d")
            waktu = now.strftime("%H:%M:%S")

            # Check if already has absensi today
            if AbsensiQueries.check_existing_absensi(nim, tanggal):
                return "SUDAH_ABSEN", nama

            # Insert new absensi
            AbsensiQueries.insert_absensi(nim, tanggal, waktu, keterangan)
            return "SUKSES", nama
        else:
            return "NIM_TIDAK_ADA", ""

    @staticmethod
    def get_all_records() -> List[Tuple]:
        """Get all absensi records"""
        return AbsensiQueries.get_all_absensi()

    @staticmethod
    def search_records(keyword: str) -> List[Tuple]:
        """Search absensi records by keyword"""
        return AbsensiQueries.search_absensi(keyword)
