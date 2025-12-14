import csv
import customtkinter as ctk
from tkinter import messagebox, filedialog, simpledialog
from typing import Optional
from app.services import MahasiswaService, AbsensiService

# Modern color scheme
CTK_FG_COLOR = "#ECF0F1"
CTK_BG_COLOR = "#2C3E50"
CTK_BUTTON_COLOR = "#3498DB"
CTK_BUTTON_HOVER = "#2980B9"
CTK_SUCCESS_COLOR = "#27AE60"
CTK_ERROR_COLOR = "#E74C3C"
CTK_WARNING_COLOR = "#F39C12"


class AplikasiAbsensiModern:
    # Modern application GUI using CustomTkinter
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Absensi - Kelompok 3")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        # Set modern theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Main container
        main_container = ctk.CTkFrame(root, fg_color=CTK_BG_COLOR)
        main_container.pack(side="top", fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(main_container, fg_color="#1A252F", height=60)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="📋 Aplikasi Absensi - Kelompok 3",
            font=("Segoe UI", 20, "bold"),
            text_color=CTK_FG_COLOR,
        )
        title.pack(side="left", padx=20, pady=10)

        # Tabs
        self.tabs = ctk.CTkTabview(main_container, fg_color=CTK_BG_COLOR)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab1 = self.tabs.add("📝 Isi Kehadiran")
        self.tab2 = self.tabs.add("👥 Daftar Mahasiswa")
        self.tab3 = self.tabs.add("📊 Rekap Laporan")

        # Setup tabs
        self.setup_tab_absensi_modern()
        self.setup_tab_daftar_modern()
        self.setup_tab_laporan_modern()

        # Bottom button container
        footer = ctk.CTkFrame(main_container, fg_color="#1A252F")
        footer.pack(fill="x", padx=10, pady=10)

        close_btn = ctk.CTkButton(
            footer,
            text="❌ Close App",
            command=self.root.destroy,
            fg_color=CTK_ERROR_COLOR,
            hover_color="#C0392B",
            font=("Segoe UI", 12, "bold"),
        )
        close_btn.pack(side="right", padx=5)

        self.load_laporan()

    def setup_tab_absensi_modern(self):
        # Modern attendance tab with improved layout
        self.tab1.configure(fg_color=CTK_BG_COLOR)

        # Search & Filter Frame
        filter_frame = ctk.CTkFrame(self.tab1, fg_color="#34495E", corner_radius=10)
        filter_frame.pack(fill="x", padx=10, pady=10)

        # Search
        search_label = ctk.CTkLabel(
            filter_frame,
            text="🔍 Cari Nama/NIM:",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
        )
        search_label.pack(side="left", padx=10, pady=8)

        self.absen_search = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Ketik NIM atau nama...",
            width=200,
            corner_radius=8,
        )
        self.absen_search.pack(side="left", padx=5, pady=8)

        search_btn = ctk.CTkButton(
            filter_frame,
            text="Cari",
            command=self._absen_reload_filtered,
            width=70,
            fg_color=CTK_BUTTON_COLOR,
            hover_color=CTK_BUTTON_HOVER,
        )
        search_btn.pack(side="left", padx=5, pady=8)

        # Sort
        sort_label = ctk.CTkLabel(
            filter_frame,
            text="🔤 Urut:",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
        )
        sort_label.pack(side="left", padx=15, pady=8)

        self.absen_sort = ctk.CTkComboBox(
            filter_frame,
            values=[
                "NIM ASC",
                "NIM DESC",
                "Nama ASC",
                "Nama DESC",
                "Status ASC",
                "Status DESC",
            ],
            command=lambda _: self._absen_reload_filtered(),
            width=130,
            corner_radius=8,
        )
        self.absen_sort.set("NIM ASC")
        self.absen_sort.pack(side="left", padx=5, pady=8)

        reset_btn = ctk.CTkButton(
            filter_frame,
            text="Reset",
            command=self._absen_reset_filters,
            width=70,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
        )
        reset_btn.pack(side="left", padx=5, pady=8)

        # List area with scrollbar
        list_frame = ctk.CTkFrame(self.tab1, fg_color=CTK_BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.absen_scrollable = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="#34495E",
            corner_radius=10,
            label_text="Daftar Mahasiswa",
            label_font=("Segoe UI", 12, "bold"),
        )
        self.absen_scrollable.pack(fill="both", expand=True)

        # Store for row references
        self.status_vars = {}
        self.displayed_rows = []
        self.absen_rows_frame = self.absen_scrollable

        # Bottom action frame
        action_frame = ctk.CTkFrame(self.tab1, fg_color="#34495E", corner_radius=10)
        action_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_info = ctk.CTkLabel(
            action_frame,
            text="✓ Status default semua: Alfa",
            text_color=CTK_SUCCESS_COLOR,
            font=("Segoe UI", 11),
        )
        self.lbl_info.pack(side="left", padx=15, pady=10)

        save_btn = ctk.CTkButton(
            action_frame,
            text="💾 Save",
            command=self._absen_submit_all,
            fg_color=CTK_SUCCESS_COLOR,
            hover_color="#229954",
            font=("Segoe UI", 12, "bold"),
        )
        save_btn.pack(side="right", padx=15, pady=10)

        # Initial load
        self._absen_load_rows()

    def _absen_load_rows(
        self,
        keyword: Optional[str] = None,
        sort_field: str = "nim",
        sort_dir: str = "ASC",
    ):
        # Clear previous rows
        for widget in self.absen_rows_frame.winfo_children():
            widget.destroy()
        self.status_vars.clear()
        self.displayed_rows = []

        rows = MahasiswaService.list_mahasiswa(keyword, sort_field, sort_dir)

        if not rows:
            empty_label = ctk.CTkLabel(
                self.absen_rows_frame,
                text="📭 Tidak ada mahasiswa",
                text_color="#BDC3C7",
                font=("Segoe UI", 12),
            )
            empty_label.pack(pady=20)
            return

        # Header
        header_frame = ctk.CTkFrame(self.absen_rows_frame, fg_color="#2C3E50")
        header_frame.pack(fill="x", padx=5, pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="NIM",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
            width=100,
        ).pack(side="left", padx=8, pady=8)
        ctk.CTkLabel(
            header_frame,
            text="Nama",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
            width=200,
        ).pack(side="left", padx=8, pady=8)
        ctk.CTkLabel(
            header_frame,
            text="Status",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
            width=300,
        ).pack(side="left", padx=8, pady=8)

        # Data rows
        for idx, (nim, nama, jur) in enumerate(rows):
            var = ctk.StringVar(value="Alfa")
            self.status_vars[nim] = var

            row_frame = ctk.CTkFrame(
                self.absen_rows_frame,
                fg_color="#3A4D63" if idx % 2 == 0 else "#34495E",
                corner_radius=6,
            )
            row_frame.pack(fill="x", padx=5, pady=3)

            nim_label = ctk.CTkLabel(
                row_frame,
                text=nim,
                text_color=CTK_FG_COLOR,
                font=("Segoe UI", 10),
                width=100,
            )
            nim_label.pack(side="left", padx=8, pady=10)

            nama_label = ctk.CTkLabel(
                row_frame,
                text=nama,
                text_color=CTK_FG_COLOR,
                font=("Segoe UI", 10),
                width=200,
            )
            nama_label.pack(side="left", padx=8, pady=10)

            status_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            status_frame.pack(side="left", padx=8, pady=10)

            for st in ["Alfa", "Hadir", "Izin", "Sakit"]:
                rb = ctk.CTkRadioButton(
                    status_frame,
                    text=st,
                    variable=var,
                    value=st,
                    font=("Segoe UI", 10),
                    width=80,
                )
                rb.pack(side="left", padx=3)

            self.displayed_rows.append(row_frame)

        # Sort by status
        sel = self.absen_sort.get()
        if sel.startswith("Status"):
            reverse = sel.endswith("DESC")
            body_sorted = sorted(
                enumerate(self.displayed_rows),
                key=lambda x: self.status_vars[rows[x[0]][0]].get(),
                reverse=reverse,
            )
            for fr in self.displayed_rows:
                fr.pack_forget()
            for _, fr in body_sorted:
                fr.pack(fill="x", padx=5, pady=3)

    def _absen_reset_filters(self):
        self.absen_search.delete(0, "end")
        self.absen_sort.set("NIM ASC")
        self._absen_reload_filtered()

    def _absen_reload_filtered(self):
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
        status_map = {}
        for nim in self.status_vars.keys():
            status_map[nim] = self.status_vars[nim].get()

        if not status_map:
            messagebox.showwarning("Kosong", "Tidak ada mahasiswa untuk disubmit.")
            return

        count = AbsensiService.apply_statuses_for_today(status_map)
        self.lbl_info.configure(
            text=f"✓ Sukses submit {count} status.", text_color=CTK_SUCCESS_COLOR
        )
        self.load_laporan()

    def setup_tab_daftar_modern(self):
        # Modern registration & deletion tab
        self.tab2.configure(fg_color=CTK_BG_COLOR)

        # Add student section
        add_frame = ctk.CTkFrame(self.tab2, fg_color="#34495E", corner_radius=10)
        add_frame.pack(fill="x", padx=10, pady=10)

        add_title = ctk.CTkLabel(
            add_frame,
            text="➕ Tambah Mahasiswa Baru",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 13, "bold"),
        )
        add_title.pack(pady=10)

        # Form inputs
        form_container = ctk.CTkFrame(add_frame, fg_color="transparent")
        form_container.pack(fill="x", padx=20, pady=10)

        # NIM
        ctk.CTkLabel(
            form_container,
            text="NIM:",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(10, 2))
        self.ent_reg_nim = ctk.CTkEntry(
            form_container,
            placeholder_text="Masukkan NIM...",
            corner_radius=8,
        )
        self.ent_reg_nim.pack(fill="x", pady=5)

        # Nama
        ctk.CTkLabel(
            form_container,
            text="Nama Lengkap:",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(10, 2))
        self.ent_reg_nama = ctk.CTkEntry(
            form_container,
            placeholder_text="Masukkan nama...",
            corner_radius=8,
        )
        self.ent_reg_nama.pack(fill="x", pady=5)

        # Jurusan
        ctk.CTkLabel(
            form_container,
            text="Jurusan/Kelas:",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(10, 2))
        self.ent_reg_jurusan = ctk.CTkEntry(
            form_container,
            placeholder_text="Masukkan jurusan...",
            corner_radius=8,
        )
        self.ent_reg_jurusan.pack(fill="x", pady=5)

        # Save button
        save_btn = ctk.CTkButton(
            form_container,
            text="💾 Simpan Data Mahasiswa",
            command=self.proses_daftar,
            fg_color=CTK_BUTTON_COLOR,
            hover_color=CTK_BUTTON_HOVER,
            font=("Segoe UI", 12, "bold"),
        )
        save_btn.pack(fill="x", pady=15)

        # Separator
        sep = ctk.CTkFrame(self.tab2, fg_color="#7F8C8D", height=2)
        sep.pack(fill="x", padx=20, pady=10)

        # Delete student section
        del_frame = ctk.CTkFrame(self.tab2, fg_color="#34495E", corner_radius=10)
        del_frame.pack(fill="x", padx=10, pady=10)

        del_title = ctk.CTkLabel(
            del_frame,
            text="🗑️ Hapus Mahasiswa",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 13, "bold"),
        )
        del_title.pack(pady=10)

        del_container = ctk.CTkFrame(del_frame, fg_color="transparent")
        del_container.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            del_container,
            text="Masukkan NIM:",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(10, 2))

        self.ent_del_nim = ctk.CTkEntry(
            del_container,
            placeholder_text="Masukkan NIM yang akan dihapus...",
            corner_radius=8,
        )
        self.ent_del_nim.pack(fill="x", pady=5)

        del_btn = ctk.CTkButton(
            del_container,
            text="❌ Delete Mahasiswa",
            command=self.proses_delete_mahasiswa,
            fg_color=CTK_ERROR_COLOR,
            hover_color="#C0392B",
            font=("Segoe UI", 12, "bold"),
        )
        del_btn.pack(fill="x", pady=15)

    def proses_daftar(self):
        nim = self.ent_reg_nim.get().strip()
        nama = self.ent_reg_nama.get().strip()
        jurusan = self.ent_reg_jurusan.get().strip()

        if nim and nama:
            success = MahasiswaService.register_mahasiswa(nim, nama, jurusan)
            if success:
                messagebox.showinfo("✓ Sukses", f"Data {nama} berhasil disimpan!")
                self.ent_reg_nim.delete(0, "end")
                self.ent_reg_nama.delete(0, "end")
                self.ent_reg_jurusan.delete(0, "end")
                self._absen_reload_filtered()
            else:
                messagebox.showerror("❌ Error", "NIM sudah terdaftar!")
        else:
            messagebox.showwarning("⚠️ Peringatan", "NIM dan Nama harus diisi!")

    def proses_delete_mahasiswa(self):
        nim = self.ent_del_nim.get().strip()
        if not nim:
            messagebox.showwarning("⚠️ Peringatan", "Masukkan NIM yang akan dihapus.")
            return

        confirm = simpledialog.askstring(
            "🔐 Konfirmasi", "Ketik ulang NIM untuk konfirmasi hapus:"
        )
        if confirm is None:
            return
        if confirm.strip() != nim:
            messagebox.showerror("❌ Error", "NIM konfirmasi tidak cocok.")
            return

        if MahasiswaService.delete_mahasiswa(nim):
            messagebox.showinfo("✓ Sukses", f"Mahasiswa NIM {nim} berhasil dihapus.")
            self.ent_del_nim.delete(0, "end")
            self._absen_reload_filtered()
        else:
            messagebox.showerror("❌ Error", "NIM tidak ditemukan atau gagal dihapus.")

    def setup_tab_laporan_modern(self):
        # Modern report tab
        self.tab3.configure(fg_color=CTK_BG_COLOR)

        # Search section
        search_frame = ctk.CTkFrame(self.tab3, fg_color="#34495E", corner_radius=10)
        search_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            search_frame,
            text="🔍 Cari Laporan:",
            text_color=CTK_FG_COLOR,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left", padx=10, pady=8)

        self.ent_cari = ctk.CTkEntry(
            search_frame,
            placeholder_text="Cari nama atau NIM...",
            width=250,
            corner_radius=8,
        )
        self.ent_cari.pack(side="left", padx=5, pady=8)

        search_btn = ctk.CTkButton(
            search_frame,
            text="Cari",
            command=self.proses_cari,
            width=70,
            fg_color=CTK_BUTTON_COLOR,
            hover_color=CTK_BUTTON_HOVER,
        )
        search_btn.pack(side="left", padx=5, pady=8)

        refresh_btn = ctk.CTkButton(
            search_frame,
            text="🔄 Refresh",
            command=self.load_laporan,
            width=70,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
        )
        refresh_btn.pack(side="left", padx=5, pady=8)

        export_btn = ctk.CTkButton(
            search_frame,
            text="📥 Export CSV",
            command=self.export_ke_csv,
            width=100,
            fg_color=CTK_SUCCESS_COLOR,
            hover_color="#229954",
        )
        export_btn.pack(side="right", padx=5, pady=8)

        # Table section
        table_frame = ctk.CTkFrame(self.tab3, fg_color=CTK_BG_COLOR)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Treeview for modern table
        from tkinter import ttk

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#34495E",
            foreground=CTK_FG_COLOR,
            rowheight=25,
            fieldbackground="#34495E",
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading", background="#2C3E50", foreground=CTK_FG_COLOR
        )
        style.map("Treeview", background=[("selected", "#3498DB")])

        columns = ("Tanggal", "Jam", "NIM", "Nama", "Ket")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=20
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def proses_cari(self):
        keyword = self.ent_cari.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = (
            AbsensiService.search_records(keyword)
            if keyword
            else AbsensiService.get_all_records()
        )
        for row in rows:
            self.tree.insert("", "end", values=row)

    def load_laporan(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = AbsensiService.get_all_records()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def export_ke_csv(self):
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
                messagebox.showinfo(
                    "✓ Sukses", f"Data berhasil diexport ke {file_path}"
                )
            except Exception as e:
                messagebox.showerror("❌ Error", f"Gagal export: {e}")
