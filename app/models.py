# Data models for the application
from dataclasses import dataclass
from typing import Optional


@dataclass
class Mahasiswa:
    # Mahasiswa data model
    nim: str
    nama: str
    jurusan: Optional[str] = None


@dataclass
class Absensi:
    # Absensi data model
    nim: str
    tanggal: str
    waktu: str
    keterangan: str
    id: Optional[int] = None


@dataclass
class AbsensiRecord:
    # Complete absensi record with student information
    tanggal: str
    waktu: str
    nim: str
    nama: str
    keterangan: str
