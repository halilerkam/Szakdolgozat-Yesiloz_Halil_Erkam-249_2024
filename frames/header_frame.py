import customtkinter as ctk
import session
import header as h
import frames.edit_task_frame as etf
from tkinter import messagebox
from database_helper import DatabaseHelper

class HeaderFrame(ctk.CTkFrame):
    def __init__(self, parent, title, navigate_callback, *args, **kwargs):
        super().__init__(parent, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND, *args, **kwargs)
        self.navigate_callback = navigate_callback
        self.db_helper = DatabaseHelper()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0, minsize=60)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0, minsize=60)
        
        back = h.ARROW_LEFT
        self.back_button = ctk.CTkButton(self, text="", image=back, command=lambda: None, width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.PALE_PURPLE, hover_color=h.LIGHT_PURPLE, height=60)
        self.back_button.grid(row=0, column=0, padx=0)
        self.back_button.grid_remove()
        
        logo = h.LOGO_ICON
        self.icon_label = ctk.CTkLabel(self, image=logo, text="")
        self.icon_label.grid(row=0, column=0, padx=(20,10), pady=(1,0), sticky="nesw")

        self.title_label = ctk.CTkLabel(self, text=title, font=("Montserrat", 30, "bold"), width=300, wraplength=300, anchor="w", justify="left")
        self.title_label.grid(row=0, column=1, padx=10, sticky="w")

        profile = h.PROFILE
        self.profile_button = ctk.CTkButton(self, text="", image=profile, command=self.go_to_profile, font=("Montserrat", 12), anchor="e", width=30, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, hover_color=h.COLOR_BACKGROUND)
        self.profile_button.grid(row=0, column=2, padx=(10, 24), sticky="e")

        if session.current_user_id != None:
            #self.user_data = session.get_current_user_data(session.current_user_id)
            self.current_points = self.db_helper.get_current_points()

            collab_stars = h.COLLAB_STARS
            self.collab_stars_icon = ctk.CTkLabel(self, text=f"  {self.current_points}", font=("Montserrat", 18, "bold"), image=collab_stars, anchor="e", compound="left", width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
            self.collab_stars_icon.grid(row=0, column=2, padx=(10, 24), sticky="e")
            self.collab_stars_icon.grid_forget()

    """ def go_back(self):
        if self.title_label.cget("text") == "Profil":
            self.navigate_callback("main")
            self.profile_button.grid(row=0, column=2, padx=10, sticky="e")
            self.icon_label.grid() """

    def go_to_profile(self):
        self.navigate_callback("profile")
        self.back_button.grid(row=0, column=0, padx=(20,10))
        self.profile_button.grid_remove()
        self.icon_label.grid_remove()
        self.collab_stars_icon.grid(row=0, column=2, padx=(10, 24), sticky="e")
        self.collab_stars_icon.configure(text=self.db_helper.get_current_points())
        

    def update_title(self, new_title):
        if new_title == "Új feladat hozzáadása":
            self.title_label.configure(text=new_title, font=("Montserrat", 24, "bold"))
            self.back_button.grid(row=0, column=0, padx=(20,10))
            self.icon_label.grid_remove()
        elif new_title == "Feladat részletei":
            self.title_label.configure(text=new_title, font=("Montserrat", 30, "bold"))
            self.back_button.grid(row=0, column=0, padx=(20,10))
            self.icon_label.grid_remove()
        else:

            self.title_label.configure(text=new_title, font=("Montserrat", 30, "bold"))
    
    def update_back_button(self, destination=None, origin=None):
        if destination:
            self.back_button.configure(command=lambda: self.navigate_callback(destination))
            self.profile_button.grid()
            self.collab_stars_icon.grid_forget()
            self.icon_label.grid(row=0, column=0, padx=(20,10), sticky="nesw")
        else:
            self.back_button.grid_remove()
            self.profile_button.grid()
            self.collab_stars_icon.grid_forget()
            self.icon_label.grid(row=0, column=0, padx=(20,10), sticky="nesw")
