import customtkinter as ctk
import tkinter as tk
from tkinter import PhotoImage
from auth import login_user
from tkinter import messagebox
import re
import header as h

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, navigate, db_helper, *args, **kwargs):
        super().__init__(parent, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND, *args, **kwargs)
        
        self.on_login_success = on_login_success
        self.navigate = navigate
        
        self.db_helper = db_helper

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0, minsize=120)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0, minsize=50)

        self.login_window_frame = ctk.CTkFrame(self, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND)
        self.login_window_frame.columnconfigure(0, weight=1)
        self.login_window_frame.rowconfigure(0, weight=1)
        self.login_window_frame.grid(row=0, column=0, sticky="nsew")

        main_logo = h.MAIN_LOGO
        if main_logo:
            self.main_logo = ctk.CTkLabel(self.login_window_frame, image=main_logo, text="", width=600)
            self.main_logo.grid(row=0, column=0, padx=0, pady=(80, 60), sticky="nesw")

        self.no_connection_label = ctk.CTkLabel(self, text="Nincs csatlakozás az adatbázishoz. Ellenőrizze a hálózatát és indítsa újra az alkalmazást.", font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, corner_radius=10, wraplength=500, text_color=h.SOFT_WHITE)
        self.no_connection_label.grid(row=2, column=0, padx=16, pady=8, sticky="nsew")
        self.no_connection_label.grid_forget()

        self.login_form_frame = ctk.CTkFrame(self.login_window_frame, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND)
        self.login_form_frame.columnconfigure(0, weight=1)
        self.login_form_frame.rowconfigure(0, weight=1)
        self.login_form_frame.grid(row=1, column=0, padx=80, sticky="nsew")
        
        self.login_form_frame.rowconfigure(1, weight=1)
        self.login_form_frame.rowconfigure(2, weight=1)
        self.login_form_frame.rowconfigure(3, weight=1)
        self.login_form_frame.rowconfigure(4, weight=1)
        
        self.alcim_bejelentkezes = ctk.CTkLabel(self.login_form_frame, text="Bejelentkezés", font=("Montserrat", 32, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.alcim_bejelentkezes.grid(row=1, column=0, pady=8, sticky="w")

        self.email_entry = ctk.CTkEntry(self.login_form_frame, placeholder_text="Email cím...", font=("Montserrat", 13), corner_radius=10, border_color=h.MEDIUM_GREY, height=60)
        self.email_entry.grid(row=2, column=0, pady=8, sticky="nesw")
        
        self.jelszo_entry = ctk.CTkEntry(self.login_form_frame, placeholder_text="Jelszó...", font=("Montserrat", 13), corner_radius=10, border_color=h.MEDIUM_GREY, height=60, show="*")
        self.jelszo_entry.grid(row=3, column=0, pady=8, sticky="nesw")

        nyil = h.ARROW_RIGHT
        self.bejelentkezes_gomb = ctk.CTkButton(self.login_form_frame, text="", image=nyil, height=80, border_width=0, corner_radius=15, fg_color=h.LIGHT_PURPLE, text_color=h.GREY_TEXT, hover_color=h.PALE_PURPLE, bg_color=h.COLOR_BACKGROUND, command=self.login_action)
        self.bejelentkezes_gomb.grid(row=4, column=0, pady=8, sticky="nesw")
        
        self.regisztracio_gomb = ctk.CTkButton(self.login_form_frame, text="Nincs még fiókom", font=("Montserrat", 16), height=20, text_color="grey50", hover_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND, command=lambda: self.navigate("register"))
        self.regisztracio_gomb.grid(row=5, column=0, pady=16)

        self.master

        if self.db_helper.check_connection() == False:
            self.no_connection_label.grid(row=2, column=0, padx=16, pady=8, sticky="nsew")
            self.email_entry.configure(state="disabled")
            self.jelszo_entry.configure(state="disabled")
            self.bejelentkezes_gomb.configure(state="disabled")
            self.regisztracio_gomb.configure(state="disabled")
        
    def login_action(self):
        
        email = self.email_entry.get()
        password = self.jelszo_entry.get()

        if email == "" or password == "":
            messagebox.showerror("Hiba", "Kérjük, adja meg az e-mail címet és a jelszót!")
            return
        
        if not is_valid_email(email):
            messagebox.showerror("Hiba", "Kérjük, adjon meg érvényes e-mail címet!")
            return
        
        success = login_user(email, password)

        if success:
            self.email_entry.delete(0, tk.END)
            self.jelszo_entry.delete(0, tk.END)
            self.on_login_success()
        else:
            messagebox.showerror("Belépés sikertelen", "Hibás e-mail cím vagy jelszó!")