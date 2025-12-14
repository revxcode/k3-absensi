# Main entry point for the application
import customtkinter as ctk
from app.database import Database
from app.gui import AplikasiAbsensiModern


def main():
    # Main function to run the application
    # Initialize database
    Database.init_db()

    # Create and run modern GUI
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = AplikasiAbsensiModern(root)
    root.mainloop()


if __name__ == "__main__":
    main()
