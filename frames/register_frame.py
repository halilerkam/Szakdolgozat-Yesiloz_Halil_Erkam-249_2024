import customtkinter as ctk
from auth import register_user
from tkinter import messagebox
import re
import header as h

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, navigate, db_helper, *args, **kwargs):
        super().__init__(parent, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND, *args, **kwargs)

        self.navigate = navigate
        self.db_helper = db_helper

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0, minsize=120)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0, minsize=50)

        self.register_window_frame = ctk.CTkFrame(self, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND)
        self.register_window_frame.columnconfigure(0, weight=1)
        self.register_window_frame.rowconfigure(0, weight=1)
        self.register_window_frame.grid(row=0, column=0, sticky="nsew")

        main_logo = h.MAIN_LOGO
        if main_logo:
            self.main_logo = ctk.CTkLabel(self.register_window_frame, image=main_logo, text="", width=600)
            self.main_logo.grid(row=0, column=0, padx=0, pady=(80, 60), sticky="nesw")

        self.no_connection_label = ctk.CTkLabel(self, text="Nincs csatlakozás az adatbázishoz. Nem hozhat létre fiókot. Ellenőrizze a hálózatát és indítsa újra az alkalmazást.", font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, corner_radius=10, text_color=h.SOFT_WHITE)
        self.no_connection_label.grid(row=2, column=0, padx=16, pady=8, sticky="nsew")
        self.no_connection_label.grid_forget()

        self.register_form_frame = ctk.CTkFrame(self.register_window_frame, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND)
        self.register_form_frame.columnconfigure(0, weight=1)
        self.register_form_frame.rowconfigure(0, weight=1)
        self.register_form_frame.grid(row=1, column=0, padx=80, sticky="nsew")
        
        self.register_form_frame.rowconfigure(1, weight=1)
        self.register_form_frame.rowconfigure(2, weight=1)
        self.register_form_frame.rowconfigure(3, weight=1)
        self.register_form_frame.rowconfigure(4, weight=1)
        self.register_form_frame.rowconfigure(5, weight=1)
        self.register_form_frame.rowconfigure(6, weight=1)
        self.register_form_frame.rowconfigure(7, weight=1)
        
        self.alcim_bejelentkezes = ctk.CTkLabel(self.register_form_frame, text="Regisztráció", font=("Montserrat", 32, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.alcim_bejelentkezes.grid(row=1, column=0, pady=8, sticky="w")

        self.keresztnev_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Keresztnév...", font=("Montserrat", 13), height=60, corner_radius=10, border_color=h.MEDIUM_GREY)
        self.keresztnev_entry.grid(row=2, column=0, pady=8, sticky="nesw")

        self.vezeteknev_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Vezeteknév...", font=("Montserrat", 13), height=60, corner_radius=10, border_color=h.MEDIUM_GREY)
        self.vezeteknev_entry.grid(row=3, column=0, pady=8, sticky="nesw")

        self.email_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Email cím...", font=("Montserrat", 13), height=60, corner_radius=10, border_color=h.MEDIUM_GREY)
        self.email_entry.grid(row=4, column=0, pady=8, sticky="nesw")
        
        self.jelszo_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Jelszó...", font=("Montserrat", 13), height=60, corner_radius=10, border_color=h.MEDIUM_GREY, show="*")
        self.jelszo_entry.grid(row=5, column=0, pady=8, sticky="nesw")

        nyil = h.ARROW_RIGHT
        self.regisztralas_gomb = ctk.CTkButton(self.register_form_frame, text="", image=nyil, font=("Montserrat", 16), height=80, border_width=0, corner_radius=15, fg_color=h.LIGHT_PURPLE, text_color=h.GREY_TEXT, hover_color=h.PALE_PURPLE, bg_color=h.COLOR_BACKGROUND, command=self.register_action)
        self.regisztralas_gomb.grid(row=6, column=0, pady=8, sticky="nesw")
        
        self.bejelentkezo_gomb = ctk.CTkButton(self.register_form_frame, text="Van már fiókom", font=("Montserrat", 16), height=16, text_color="grey50", hover_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND, command=lambda: self.navigate("login"))
        self.bejelentkezo_gomb.grid(row=7, column=0, pady=16)

        if self.db_helper.check_connection() == False:
            self.no_connection_label.grid(row=2, column=0, padx=16, pady=8, sticky="nsew")
            self.keresztnev_entry.configure(state="disabled")
            self.vezeteknev_entry.configure(state="disabled")
            self.email_entry.configure(state="disabled")
            self.jelszo_entry.configure(state="disabled")
            self.regisztralas_gomb.configure(state="disabled")
            self.bejelentkezo_gomb.configure(state="disabled")


    def register_action(self):
        firstname = self.keresztnev_entry.get()
        lastname = self.vezeteknev_entry.get()
        email = self.email_entry.get()
        password = self.jelszo_entry.get()

        if not firstname or not lastname or not email or not password:
            messagebox.showerror("Hiba", "Minden mező kitöltése kötelező.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Hiba", "Kérjük, adjon meg érvényes e-mail címet!")
            return

        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
            messagebox.showerror("Hiba", "A jelszónak minimum 8 karakter hosszúnak kell lennie, tartalmaznia kell legalább egy számot és egy nagybetűt.")
            return

        success = register_user(firstname, lastname, email, password)
        if success:
            messagebox.showinfo("Sikeres regisztráció", "A regisztráció sikeresen megtörtént.")
            self.navigate("login")
        else:
            messagebox.showerror("Hiba", "A regisztráció sikertelen. Az email cím már foglalt lehet.")

