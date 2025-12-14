"""
GUI module for the application
"""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from app.services import MahasiswaService, AbsensiService


class AplikasiAbsensi:
    """Main application GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Absensi - Kelompok 3")
        self.root.geometry("600x400")

        # Create tabs
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=1, fill="both")

        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text="Isi Kehadiran")
        self.tabs.add(self.tab2, text="Daftar Mahasiswa Baru")
        self.tabs.add(self.tab3, text="Rekap Laporan")

        self.setup_tab_absensi()
        self.setup_tab_daftar()
        self.setup_tab_laporan()

        self.load_laporan()

    def setup_tab_absensi(self):
        """Setup attendance tab"""
        frame = ttk.Frame(self.tab1, padding=20)
        frame.pack()

        ttk.Label(frame, text="Masukkan NIM untuk Absen:", font=("Helvetica", 12)).pack(
            pady=5
        )

        self.entry_nim_absen = ttk.Entry(frame, font=("Helvetica", 14))
        self.entry_nim_absen.pack(pady=5)
        self.entry_nim_absen.focus()

        ttk.Label(frame, text="Status Kehadiran:").pack(pady=5)
        self.combo_status = ttk.Combobox(frame, values=["Hadir", "Izin", "Sakit"])
        self.combo_status.current(0)
        self.combo_status.pack(pady=5)

        ttk.Button(frame, text="SUBMIT ABSENSI", command=self.proses_absen).pack(
            pady=20
        )

        self.lbl_info = ttk.Label(
            frame, text="Siap menerima input...", foreground="blue"
        )
        self.lbl_info.pack()

    def setup_tab_daftar(self):
        """Setup student registration tab"""
        frame = ttk.Frame(self.tab2, padding=20)
        frame.pack()

        ttk.Label(frame, text="NIM:").pack(anchor="w")
        self.ent_reg_nim = ttk.Entry(frame, width=30)
        self.ent_reg_nim.pack(pady=5)

        ttk.Label(frame, text="Nama Lengkap:").pack(anchor="w")
        self.ent_reg_nama = ttk.Entry(frame, width=30)
        self.ent_reg_nama.pack(pady=5)

        ttk.Label(frame, text="Jurusan/Kelas:").pack(anchor="w")
        self.ent_reg_jurusan = ttk.Entry(frame, width=30)
        self.ent_reg_jurusan.pack(pady=5)

        ttk.Button(
            frame, text="Simpan Data Mahasiswa", command=self.proses_daftar
        ).pack(pady=20)

    def setup_tab_laporan(self):
        """Setup report tab"""
        frame_cari = ttk.Frame(self.tab3)
        frame_cari.pack(pady=5)

        self.ent_cari = ttk.Entry(frame_cari, width=20)
        self.ent_cari.pack(side="left", padx=5)

        ttk.Button(frame_cari, text="Cari Nama/NIM", command=self.proses_cari).pack(
            side="left"
        )

        # Treeview table
        columns = ("Tanggal", "Jam", "NIM", "Nama", "Ket")
        self.tree = ttk.Treeview(self.tab3, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        btn_refresh = ttk.Button(
            self.tab3, text="Refresh Data", command=self.load_laporan
        )
        btn_refresh.pack(pady=5)

        btn_export = ttk.Button(
            self.tab3, text="Export ke CSV", command=self.export_ke_csv
        )
        btn_export.pack(pady=5)

    def proses_daftar(self):
        """Process student registration"""
        nim = self.ent_reg_nim.get()
        nama = self.ent_reg_nama.get()
        jurusan = self.ent_reg_jurusan.get()

        if nim and nama:
            success = MahasiswaService.register_mahasiswa(nim, nama, jurusan)
            if success:
                messagebox.showinfo("Sukses", f"Data {nama} berhasil disimpan!")
                self.ent_reg_nim.delete(0, "end")
                self.ent_reg_nama.delete(0, "end")
                self.ent_reg_jurusan.delete(0, "end")
            else:
                messagebox.showerror("Error", "NIM sudah terdaftar!")
        else:
            messagebox.showwarning("Peringatan", "NIM dan Nama harus diisi!")

    def proses_absen(self):
        """Process attendance submission"""
        nim = self.entry_nim_absen.get()
        keterangan = self.combo_status.get()

        if nim:
            status, nama = AbsensiService.submit_absensi(nim, keterangan)

            if status == "SUKSES":
                self.lbl_info.config(
                    text=f"Sukses: {nama} berhasil absen ({keterangan})",
                    foreground="green",
                )
                self.entry_nim_absen.delete(0, "end")
                self.load_laporan()
            elif status == "SUDAH_ABSEN":
                self.lbl_info.config(
                    text=f"Info: {nama} sudah absen hari ini.", foreground="orange"
                )
                messagebox.showinfo("Info", "Anda sudah absen hari ini.")
            else:
                self.lbl_info.config(
                    text="Error: NIM tidak ditemukan!", foreground="red"
                )
                messagebox.showerror(
                    "Error", "NIM belum terdaftar. Silakan daftar dulu."
                )
        else:
            self.lbl_info.config(text="Masukkan NIM terlebih dahulu.", foreground="red")

    def proses_cari(self):
        """Process search"""
        keyword = self.ent_cari.get()

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get filtered data
        rows = AbsensiService.search_records(keyword)
        for row in rows:
            self.tree.insert("", "end", values=row)

    def load_laporan(self):
        """Load all records into table"""
        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get new data
        rows = AbsensiService.get_all_records()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def export_ke_csv(self):
        """Export data to CSV file"""
        rows = AbsensiService.get_all_records()

        if not rows:
            messagebox.showwarning("Kosong", "Tidak ada data untuk diexport.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if file_path:
            try:
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Tanggal", "Jam", "NIM", "Nama", "Keterangan"])
                    writer.writerows(rows)
                messagebox.showinfo("Sukses", f"Data berhasil diexport ke {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal export: {e}")
