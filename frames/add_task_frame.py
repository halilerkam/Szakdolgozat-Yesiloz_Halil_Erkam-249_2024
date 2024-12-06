import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
""" from frames.header_frame import HeaderFrame """
from frames.friend_card import FriendsCheckbox
from database_helper import DatabaseHelper
import header as h
import session

from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime

class FriendListFrame(ctk.CTkToplevel):
    def __init__(self, parent, db_helper, selected_friends=[], *args, **kwargs):
        super().__init__(parent, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)
        
        self.geometry("560x700")
        self.title("Barátok meghívása")
        self.resizable(False, False)
        self.grab_set()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (560 // 2)
        y = (screen_height // 2) - (700 // 2)

        self.geometry(f"+{x}+{y}")

        self.db_helper = db_helper
        self.selected_friends = selected_friends
        
        self.friends_list = self.db_helper.get_friends(session.current_user_id)

        self.rowconfigure(0, weight=0, minsize=60)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(self, text="Barátok meghívása", font=("Montserrat", 24, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.name_label.grid(row=0, column=0, padx=16, pady=0, columnspan=2, sticky="w")

        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND)
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(0, weight=1)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew")

        self.refresh_friends(self.friends_list)

        self.close_button = ctk.CTkButton(self, text="Mentés", command=self.save_button, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.close_button.grid(row=2, column=0, padx=10, pady=(0,10), sticky="nsew")

    def display_friends(self, friends):
        if len(friends) != 0:
            for index, friend in enumerate(friends):
                friend_data = self.db_helper.get_friend_data(friend[0])
                if friend_data != None:
                    friend_id = friend_data[0][0]
                    friend_email = friend_data[0][3]
                    friend_points = friend_data[0][5]
                    toggled_friend = False
                    for x in self.selected_friends:
                        if friend_id == x:
                            toggled_friend = True

                    friend_card = FriendsCheckbox(self.scrollable_frame, friend_id=friend_id, email=friend_email, points=friend_points, callback=self.toggle_friend_selection, toggled=toggled_friend)
                    friend_card.grid(row=index, column=0, padx=5, pady=(0,10), sticky="nsew")

    def toggle_friend_selection(self, friend_id):
        if friend_id in self.selected_friends:
            self.selected_friends.remove(friend_id)
        else:
            self.selected_friends.append(friend_id)

    def refresh_friends(self, friends):
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, FriendsCheckbox):
                widget.grid_forget()

        self.display_friends(friends)
    
    def save_button(self):
        self.destroy()



class AddTaskFrame(ctk.CTkFrame):
    def __init__(self, parent, task_list_frame, db_helper, navigate_callback, *args, **kwargs):
        super().__init__(parent, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)
        self.task_list_frame = task_list_frame
        self.db_helper = db_helper
        self.navigate_callback = navigate_callback

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0, minsize=50)

        self.task_forms_frame = ctk.CTkFrame(self, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND)
        self.task_forms_frame.columnconfigure(0, weight=1)
        self.task_forms_frame.rowconfigure(0, weight=1)
        self.task_forms_frame.grid(row=0, column=0, sticky="nsew")

        self.save_task_button = ctk.CTkButton(self, text="Feladdat létrehozása", command=self.save_task, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
        self.save_task_button.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")

        def on_hover(event):
            self.save_task_button.configure(text_color=h.GREY_TEXT, fg_color=h.PALE_PURPLE)
        def off_hover(event):
            self.save_task_button.configure(text_color="white", fg_color=h.VIVID_PURPLE)

        
        self.save_task_button.bind("<Enter>", on_hover)
        self.save_task_button.bind("<Leave>", off_hover)

        self.task_forms_frame.rowconfigure(0, weight=1)
        self.task_forms_frame.rowconfigure(1, weight=3)
        self.task_forms_frame.rowconfigure(2, weight=1)
        self.task_forms_frame.rowconfigure(3, weight=1)
        self.task_forms_frame.rowconfigure(4, weight=1)
        self.task_forms_frame.rowconfigure(5, weight=1)
        self.task_forms_frame.rowconfigure(6, weight=1)

        self.task_forms_frame.columnconfigure(0, weight=1)

        self.title_entry = ctk.CTkEntry(self.task_forms_frame, placeholder_text="Cím", font=("Montserrat", 16), text_color=h.GREY_TEXT, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.title_entry.grid(row=0, column=0, sticky="nesw", padx=16, pady=8)

        self.description_entry = ctk.CTkEntry(self.task_forms_frame, placeholder_text="Leírás", font=("Montserrat", 16), text_color=h.GREY_TEXT, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.description_entry.grid(row=1, column=0, sticky="nesw", padx=16, pady=8)

        calendar_icon = h.CALENDAR_ICON
        self.date_button = ctk.CTkButton(self.task_forms_frame, text="Dátum", font=("Montserrat", 16), image=calendar_icon, width=30, text_color=h.GREY_TEXT, anchor="w", hover_color=h.LIGHT_PURPLE, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, command=lambda: self.open_calendar_modal(self.handle_selected_date))

        self.date_button.grid(row=2, column=0, sticky="nesw", padx=16, pady=8)

        self.location_entry = ctk.CTkEntry(self.task_forms_frame, placeholder_text="Helyszín", font=("Montserrat", 16), text_color=h.GREY_TEXT, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.location_entry.grid(row=3, column=0, sticky="nesw", padx=16, pady=(10,0))

        self.priority_options = ["Alacsony", "Átlagos", "Magas"]
        self.priority_combobox = ctk.CTkOptionMenu(self.task_forms_frame, state="normal", values=self.priority_options, font=("Montserrat", 16), height=60, text_color=h.GREY_TEXT, corner_radius=10, bg_color=h.COLOR_BACKGROUND, fg_color=h.LIGHT_PURPLE, button_color=h.LIGHT_PURPLE, button_hover_color=h.PALE_PURPLE, hover=True, dropdown_fg_color=h.COLOR_BACKGROUND, dropdown_font=("Montserrat", 16), dropdown_hover_color=h.PALE_PURPLE)
        self.priority_combobox.set("Átlagos")
        self.priority_combobox.grid(row=4, column=0, sticky="sew", padx=16, pady=(0,8))

        self.environment_options = ["Beltéri tevékenység", "Kültéri tevékenység", "Család", "Személyes"]
        self.environment_combobox = ctk.CTkOptionMenu(self.task_forms_frame, state="normal", values=self.environment_options, font=("Montserrat", 16), height=60, text_color=h.GREY_TEXT, corner_radius=10, bg_color=h.COLOR_BACKGROUND, fg_color=h.LIGHT_PURPLE, button_color=h.LIGHT_PURPLE, button_hover_color=h.PALE_PURPLE, hover=True, dropdown_fg_color=h.COLOR_BACKGROUND, dropdown_font=("Montserrat", 16), dropdown_hover_color=h.PALE_PURPLE)
        self.environment_combobox.set("Beltéri tevékenység")
        self.environment_combobox.grid(row=5, column=0, sticky="sew", padx=16, pady=(0,8))

        self.invited_friends = []

        add_friend_icon = h.ADD_FRIEND
        self.friend_button = ctk.CTkButton(self.task_forms_frame, text="Barátok meghívása", font=("Montserrat", 16), image=add_friend_icon, width=60, text_color=h.GREY_TEXT, anchor="w", hover_color=h.LIGHT_PURPLE, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, command=self.open_friend_selector)
        self.friend_button.grid(row=6, column=0, sticky="nesw", padx=16, pady=8)

    def open_calendar_modal(self, callback):
        modal = ctk.CTkToplevel(self.task_forms_frame, fg_color=h.COLOR_BACKGROUND)
        modal.title("Dátum kiválasztása")
        modal.geometry("400x400")
        modal.grab_set()
        modal.resizable(False, False)
        modal.transient(self.task_forms_frame)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (400 // 2)

        modal.geometry(f"+{x}+{y}")

        modal.rowconfigure(0,weight=1)
        modal.rowconfigure(1, weight=0, minsize=60)
        modal.columnconfigure(0, weight=1)
        modal.columnconfigure(1, weight=1)

        calendar = Calendar(modal, selectmode='day', date_pattern='yyyy-mm-dd')
        calendar.pack(pady=16)

        def save_date():
            selected_date = calendar.get_date()
            callback(selected_date)
            modal.destroy()

        save_button = ctk.CTkButton(modal, text="Save Date", command=save_date, font=("Montserrat", 16), height=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, anchor="center")
        save_button.pack(pady=16)

        close_button = ctk.CTkButton(modal, text="Cancel", command=modal.destroy, font=("Montserrat", 16), height=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, anchor="center")
        close_button.pack(pady=16)
    
    def handle_selected_date(self, date):
        self.date_button.configure(text=f"{date}")
    
    def save_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        tmp_date = self.date_button.cget("text")
        if tmp_date == "Dátum":
            date = None
        else:
            date = datetime.strptime(tmp_date, "%Y-%m-%d").date()
        tmp_location = self.location_entry.get()
        if tmp_location is None:
            location = "Helyszín: -"
        else:
            location = self.location_entry.get()
        priority = self.priority_combobox.get()
        environment = self.environment_combobox.get()

        if not title or not priority:
            messagebox.showerror("Hiányzó adat", "A cím és prioritás mezőket kötelező kitölteni!")
            return

        self.db_helper.add_task(session.current_user_id, title, description, date, location, priority, environment, self.invited_friends)

        
        tasks = self.db_helper.get_all_tasks()
        self.task_list_frame.refresh_tasks(tasks)

        self.navigate_callback("main")
        
    def open_friend_selector(self):
        friend_selector = FriendListFrame(self, self.db_helper, selected_friends=self.invited_friends)
        self.wait_window(friend_selector)
        self.invited_friends = friend_selector.selected_friends
        self.update_selected_friends_label()
    
    def update_selected_friends_label(self):
        if self.invited_friends:
            self.friend_button.configure(
                text=str(len(self.invited_friends)) + " barát meghívva"
            )
        else:
            self.friend_button.configure(text="Barátok meghívása")