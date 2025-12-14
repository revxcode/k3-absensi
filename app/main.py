"""
Aplikasi Absensi - Kelompok 3
Main entry point for the application
"""

import tkinter as tk
from app.database import Database
from app.gui import AplikasiAbsensi


def main():
    """Main function to run the application"""
    # Initialize database
    Database.init_db()

    # Create and run GUI
    root = tk.Tk()
    app = AplikasiAbsensi(root)
    root.mainloop()


if __name__ == "__main__":
    main()
