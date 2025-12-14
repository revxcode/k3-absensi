# GUI module for the application
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from typing import Optional
from app.services import MahasiswaService, AbsensiService


class AplikasiAbsensi:
    # Main application GUI
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

        self.setup_tab_absensi_v2()
        self.setup_tab_daftar_v2()
        self.setup_tab_laporan()

        ttk.Button(self.root, text="Close App", command=self.root.destroy).pack(pady=5)

        self.load_laporan()

    def setup_tab_absensi(self):
        # Setup attendance tab
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
        # Setup student registration tab
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
        # Setup report tab
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
        # Process student registration
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
        # Process attendance submission
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
        # Process search
        keyword = self.ent_cari.get()

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get filtered data
        rows = AbsensiService.search_records(keyword)
        for row in rows:
            self.tree.insert("", "end", values=row)

    def load_laporan(self):
        # Load all records into table
        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get new data
        rows = AbsensiService.get_all_records()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def export_ke_csv(self):
        # Export data to CSV file
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

    # New attendance tab (v2) with list + radio buttons
    def setup_tab_absensi_v2(self):
        # Setup improved attendance tab with list, search, sort, and radio buttons
        self.absen_frame = ttk.Frame(self.tab1, padding=10)
        self.absen_frame.pack(fill="both", expand=True)

        # Top controls: search and sort
        top_controls = ttk.Frame(self.absen_frame)
        top_controls.pack(fill="x")

        ttk.Label(top_controls, text="Cari Nama/NIM:").pack(side="left", padx=5)
        self.absen_search = ttk.Entry(top_controls, width=20)
        self.absen_search.pack(side="left")

        ttk.Button(top_controls, text="Cari", command=self._absen_reload_filtered).pack(
            side="left", padx=5
        )

        ttk.Label(top_controls, text="Sort:").pack(side="left", padx=10)
        self.absen_sort = ttk.Combobox(
            top_controls,
            values=[
                "NIM ASC",
                "NIM DESC",
                "Nama ASC",
                "Nama DESC",
                "Status ASC",
                "Status DESC",
            ],
            width=12,
        )
        self.absen_sort.current(0)
        self.absen_sort.pack(side="left")
        self.absen_sort.bind(
            "<<ComboboxSelected>>", lambda e: self._absen_reload_filtered()
        )

        ttk.Button(top_controls, text="Reset", command=self._absen_reset_filters).pack(
            side="left", padx=5
        )

        # Scrollable list area
        list_container = ttk.Frame(self.absen_frame)
        list_container.pack(fill="both", expand=True, pady=10)

        self.absen_canvas = tk.Canvas(list_container)
        self.absen_scrollbar = ttk.Scrollbar(
            list_container, orient="vertical", command=self.absen_canvas.yview
        )
        self.absen_rows_frame = ttk.Frame(self.absen_canvas)

        self.absen_rows_frame.bind(
            "<Configure>",
            lambda e: self.absen_canvas.configure(
                scrollregion=self.absen_canvas.bbox("all")
            ),
        )
        self.absen_canvas.create_window(
            (0, 0), window=self.absen_rows_frame, anchor="nw"
        )
        self.absen_canvas.configure(yscrollcommand=self.absen_scrollbar.set)

        self.absen_canvas.pack(side="left", fill="both", expand=True)
        self.absen_scrollbar.pack(side="right", fill="y")

        # Bottom actions
        bottom_actions = ttk.Frame(self.absen_frame)
        bottom_actions.pack(fill="x", pady=5)

        self.lbl_info = ttk.Label(
            bottom_actions, text="Status default semua: Alfa", foreground="blue"
        )
        self.lbl_info.pack(side="left")

        ttk.Button(
            bottom_actions, text="Save/Submit Semua", command=self._absen_submit_all
        ).pack(side="right")

        # Internal state
        self.status_vars = {}
        self.displayed_rows = []

        # Initial load
        self._absen_load_rows()

    def _absen_load_rows(
        self,
        keyword: Optional[str] = None,
        sort_field: str = "nim",
        sort_dir: str = "ASC",
    ):
        # Load mahasiswa list and build rows with radio buttons
        for rf in getattr(self, "displayed_rows", []):
            try:
                rf.destroy()
            except Exception:
                pass
        self.displayed_rows = []

        rows = MahasiswaService.list_mahasiswa(keyword, sort_field, sort_dir)
        # Header
        header = ttk.Frame(self.absen_rows_frame)
        ttk.Label(header, text="NIM", width=15).pack(side="left")
        ttk.Label(header, text="Nama", width=25).pack(side="left")
        ttk.Label(header, text="Status", width=40).pack(side="left")
        header.pack(fill="x", pady=2)
        self.displayed_rows.append(header)

        for nim, nama, jur in rows:
            var = self.status_vars.get(nim)
            if not var:
                var = tk.StringVar(value="Alfa")
                self.status_vars[nim] = var

            rf = ttk.Frame(self.absen_rows_frame)
            ttk.Label(rf, text=nim, width=15).pack(side="left")
            ttk.Label(rf, text=nama, width=25).pack(side="left")

            status_frame = ttk.Frame(rf)
            status_frame.pack(side="left")
            for st in ["Alfa", "Hadir", "Izin", "Sakit"]:
                ttk.Radiobutton(status_frame, text=st, value=st, variable=var).pack(
                    side="left", padx=2
                )

            rf.pack(fill="x", pady=2)
            self.displayed_rows.append(rf)

        # Sort by status if selected
        sel = self.absen_sort.get()
        if sel.startswith("Status"):
            reverse = sel.endswith("DESC")
            body_rows = self.displayed_rows[1:]
            body_sorted = sorted(
                body_rows,
                key=lambda fr: self.status_vars[
                    fr.winfo_children()[0].cget("text")
                ].get(),
                reverse=reverse,
            )
            for fr in body_sorted:
                fr.pack_forget()
            for fr in body_sorted:
                fr.pack(fill="x", pady=2)

    def _absen_reset_filters(self):
        # Reset search and sort
        self.absen_search.delete(0, "end")
        self.absen_sort.current(0)
        self._absen_reload_filtered()

    def _absen_reload_filtered(self):
        # Reload rows based on search and sort
        keyword = self.absen_search.get().strip() or None
        sel = self.absen_sort.get()
        if sel.startswith("NIM"):
            sort_field = "nim"
            sort_dir = "DESC" if sel.endswith("DESC") else "ASC"
        elif sel.startswith("Nama"):
            sort_field = "nama"
            sort_dir = "DESC" if sel.endswith("DESC") else "ASC"
        else:
            sort_field = "nim"
            sort_dir = "ASC"
        self._absen_load_rows(keyword, sort_field, sort_dir)

    def _absen_submit_all(self):
        # Submit statuses for all displayed students
        status_map = {}
        for fr in self.displayed_rows[1:]:
            nim_label = fr.winfo_children()[0]
            nim = nim_label.cget("text")
            status_map[nim] = self.status_vars[nim].get()

        if not status_map:
            messagebox.showwarning("Kosong", "Tidak ada mahasiswa untuk disubmit.")
            return

        count = AbsensiService.apply_statuses_for_today(status_map)
        self.lbl_info.config(text=f"Sukses submit {count} status.", foreground="green")
        self.load_laporan()

    # Registration tab v2 with delete section
    def setup_tab_daftar_v2(self):
        # Setup student registration + deletion controls
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

        sep = ttk.Separator(self.tab2, orient="horizontal")
        sep.pack(fill="x", pady=10)

        del_frame = ttk.Frame(self.tab2, padding=10)
        del_frame.pack(fill="x")
        ttk.Label(del_frame, text="Hapus Mahasiswa (masukkan NIM):").pack(anchor="w")
        self.ent_del_nim = ttk.Entry(del_frame, width=30)
        self.ent_del_nim.pack(pady=5)
        ttk.Button(
            del_frame, text="Delete Mahasiswa", command=self.proses_delete_mahasiswa
        ).pack(pady=5)

    def proses_delete_mahasiswa(self):
        # Process delete mahasiswa with confirmation by re-entering NIM
        nim = getattr(self, "ent_del_nim", None)
        nim = nim.get().strip() if nim else ""
        if not nim:
            messagebox.showwarning("Peringatan", "Masukkan NIM yang akan dihapus.")
            return

        confirm = simpledialog.askstring(
            "Konfirmasi", "Ketik ulang NIM untuk konfirmasi hapus:"
        )
        if confirm is None:
            return
        if confirm.strip() != nim:
            messagebox.showerror("Error", "NIM konfirmasi tidak cocok.")
            return

        if MahasiswaService.delete_mahasiswa(nim):
            messagebox.showinfo("Sukses", f"Mahasiswa NIM {nim} berhasil dihapus.")
            self.ent_del_nim.delete(0, "end")
            self._absen_reload_filtered()
        else:
            messagebox.showerror("Error", "NIM tidak ditemukan atau gagal dihapus.")
