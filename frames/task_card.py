import customtkinter as ctk
import tkinter as tk
import header as h
from database_helper import DatabaseHelper

class TaskCard(ctk.CTkFrame):
    def __init__(self, parent, title, environment, priority, task_id, task_date, task_location, alert, navigate, done, *args, **kwargs):
        super().__init__(parent, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)

        self.task_id = task_id
        self.navigate = navigate
        self.done = done
        self.task_date = task_date
        self.task_location = task_location
        self.alert = alert

        max_length = 20
        if len(title) > max_length:
            display_title = title[:max_length] + "..."
        else:
            display_title = title

        self.title_label_var = ctk.StringVar(value=display_title)

        if environment == "Kültéri tevékenység":
            icon = h.OUTDOORS
        elif environment == "Beltéri tevékenység":
            icon = h.INDOORS
        else:
            icon = h.INDOORS  # Ha nincs megfelelő téma, akkor nincs ikon

        if priority == "Alacsony":
            priority_icon = h.PRIORITY_ICON_1
        elif priority == "Átlagos":
            priority_icon = h.PRIORITY_ICON_2
        elif priority == "Magas":
            priority_icon = h.PRIORITY_ICON_3
        else:
            priority_icon = h.PRIORITY_ICON_1  # Ha nincs megfelelő téma, akkor nincs ikon
        
        self.rowconfigure(0, weight=3)  # top row
        self.rowconfigure(1, weight=1) # bottom row
        self.columnconfigure(0, weight=1) #left column
        self.columnconfigure(1, weight=2) #mid left column
        self.columnconfigure(2, weight=1) #mid right column
        self.columnconfigure(3, weight=0, minsize=60) #far right column
        self.columnconfigure(4, weight=0, minsize=60) #far right column

        if icon:
            if self.alert != None:
                self.icon_label = ctk.CTkLabel(self, image=icon, text="", width=80)
                self.icon_label.grid(row=0, column=0, padx=(15,5), pady=8, sticky="w", rowspan=2)
            else:
                self.icon_label = ctk.CTkLabel(self, image=icon, text="", width=80)
                self.icon_label.grid(row=0, column=0, padx=(15,5), pady=8, sticky="w", rowspan=2)

        if priority_icon:
            self.priority_icon_label = ctk.CTkLabel(self, image=priority_icon, text="", width=100)
            self.priority_icon_label.grid(row=0, column=2, sticky="e", padx=(5,8), pady=(12,0))

        self.title_label = ctk.CTkLabel(self, textvariable=self.title_label_var, font=("Montserrat", 18, "bold"), width=280, wraplength=280, anchor="w")
        self.title_label.grid(row=0, column=1, padx=(10,5), pady=(12,0))

        self.location_label = ctk.CTkLabel(self, text="Budapest", font=("Montserrat", 12))
        self.location_label.grid(row=1, column=1, padx=(10,5), pady=(0,8), sticky="w")
        if task_location == "":
            self.location_label.configure(text="Helyszín: - (Időjárás nem elérhető)")
        else:
            self.location_label.configure(text=task_location)

        self.date_label = ctk.CTkLabel(self, text="", font=("Montserrat", 12), width=100)
        self.date_label.grid(row=1, column=2, padx=(5,8), pady=(0,8), sticky="e")
        self.date_label.configure(text=task_date)
        
        edit_logo = h.ARROW_RIGHT
        self.edit_button = ctk.CTkButton(self, text="", image=edit_logo, command=lambda: self.navigate(task_id), width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.PALE_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.edit_button.grid(row=0, column=3, padx=(0, 8), pady=8, sticky="nesw", rowspan=2)

        check = h.CHECK
        self.check_button = ctk.CTkButton(self, text="", image=check, command=lambda: self.done(task_id), width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.check_button.grid(row=0, column=4, padx=(0, 8), pady=8, sticky="nesw", rowspan=2)

        if self.alert != None:
            alert_button = h.WEATHER_ALERT
            badge = ctk.CTkButton(self, text="", image=alert_button, width=35, height=25, corner_radius=0, bg_color=h.VIVID_PURPLE, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE, command=self.alerting_messagebox)
            badge.place(relx=0.009, rely=0.07, anchor="nw")

    def alerting_messagebox(self):
        tk.messagebox.showinfo("Időjárás figyelmeztető", "Kinti tevékenysséghez kedvezőtlen időre számíthatunk ezen a napon. Javasolom hogy valtoztassa meg a feladat datumat.")

class CollabTaskCard(ctk.CTkFrame):
    def __init__(self, parent, title, environment, priority, task_id, task_date, task_location, alert, navigate, done, *args, **kwargs):
        super().__init__(parent, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.LIGHT_PURPLE, *args, **kwargs)

        self.task_id = task_id
        self.navigate = navigate
        self.done = done
        self.task_date = task_date
        self.task_location = task_location
        self.alert = alert

        self.db_helper = DatabaseHelper()

        self.is_creator = self.db_helper.is_creator(self.task_id)

        max_length = 20
        if len(title) > max_length:
            display_title = title[:max_length] + "..."
        else:
            display_title = title

        self.title_label_var = ctk.StringVar(value=display_title)

        if environment == "Kültéri tevékenység":
            icon = h.OUTDOORS
        elif environment == "Beltéri tevékenység":
            icon = h.INDOORS
        else:
            icon = h.INDOORS

        if priority == "Alacsony":
            priority_icon = h.PRIORITY_ICON_1
        elif priority == "Átlagos":
            priority_icon = h.PRIORITY_ICON_2
        elif priority == "Magas":
            priority_icon = h.PRIORITY_ICON_3
        else:
            priority_icon = h.PRIORITY_ICON_1
        
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0, minsize=60)
        self.columnconfigure(4, weight=0, minsize=60)

        if priority_icon:
            self.priority_icon_label = ctk.CTkLabel(self, image=priority_icon, text="", width=100)
            self.priority_icon_label.grid(row=0, column=2, sticky="e", padx=(5,8), pady=(12,0))
        
        if icon:
            self.icon_label = ctk.CTkLabel(self, image=icon, text="", width=100)
            self.icon_label.grid(row=0, column=0, padx=10, pady=(12,0), sticky="w")

        if self.is_creator:
            self.friend_label = ctk.CTkLabel(self, text="Admin", font=("Montserrat", 12), width=100, fg_color=h.LIGHT_PURPLE)
            self.friend_label.grid(row=1, column=0, padx=10, pady=(0,8), sticky="w")
        else:
            self.friend_label = ctk.CTkLabel(self, text="Meghívott", font=("Montserrat", 12), width=100, fg_color=h.LIGHT_PURPLE)
            self.friend_label.grid(row=1, column=0, padx=10, pady=(0,8), sticky="w")


        self.title_label = ctk.CTkLabel(self, textvariable=self.title_label_var, font=("Montserrat", 18, "bold"), width=280, wraplength=280, anchor="w", fg_color=h.LIGHT_PURPLE)
        self.title_label.grid(row=0, column=1, padx=5, pady=(12,0))

        self.location_label = ctk.CTkLabel(self, text="Budapest", font=("Montserrat", 12), fg_color=h.LIGHT_PURPLE)
        self.location_label.grid(row=1, column=1, padx=5, pady=(0,8), sticky="w")
        if task_location == "":
            self.location_label.configure(text="Helyszín: - (Időjárás nem elérhető)")
        else:
            self.location_label.configure(text=task_location)

        self.date_label = ctk.CTkLabel(self, text="", font=("Montserrat", 12), width=100, fg_color=h.LIGHT_PURPLE)
        self.date_label.grid(row=1, column=2, padx=(5,8), pady=(0,8), sticky="e")
        self.date_label.configure(text=task_date)

        if self.is_creator:
            edit_logo = h.ARROW_RIGHT
            self.edit_button = ctk.CTkButton(self, text="", image=edit_logo, command=lambda: self.navigate(task_id), width=60, bg_color=h.LIGHT_PURPLE, fg_color=h.PALE_PURPLE, hover_color=h.LIGHT_PURPLE)
            self.edit_button.grid(row=0, column=3, padx=(0, 8), pady=8, sticky="nesw", rowspan=2)

            check = h.CHECK
            self.check_button = ctk.CTkButton(self, text="", image=check, command=lambda: self.done(task_id), width=60, bg_color=h.LIGHT_PURPLE, fg_color=h.VIVID_PURPLE, hover_color=h.PALE_PURPLE)
            self.check_button.grid(row=0, column=4, padx=(0, 8), pady=8, sticky="nesw", rowspan=2)
        else:
            edit_logo = h.ARROW_RIGHT
            self.edit_button = ctk.CTkButton(self, text="", image=edit_logo, command=lambda: self.navigate(task_id), width=130, bg_color=h.LIGHT_PURPLE, fg_color=h.PALE_PURPLE, hover_color=h.LIGHT_PURPLE)
            self.edit_button.grid(row=0, column=3, padx=(0, 8), pady=8, sticky="nesw", rowspan=2, columnspan=2)
        
        if self.alert != None:
            alert_button = h.WEATHER_ALERT
            badge = ctk.CTkButton(self, text="", image=alert_button, width=25, height=25, corner_radius=8, bg_color=h.PALE_PURPLE, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE, command=self.alerting_messagebox)
            badge.place(relx=0, rely=0, anchor="nw")

    def alerting_messagebox(self):
        tk.messagebox.showinfo("Időjárás figyelmeztető", "Kinti tevékenysséghez kedvezőtlen időre számíthatunk ezen a napon. Javasolom hogy valtoztassa meg a feladat datumat.")

class ArchivedTaskCard(ctk.CTkFrame):
    def __init__(self, parent, title, environment, priority, task_id, undone, delete, *args, **kwargs):
        super().__init__(parent, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)
        
        self.undone = undone
        self.delete = delete

        max_length = 20
        if len(title) > max_length:
            display_title = title[:max_length] + "..."
        else:
            display_title = title

        self.title_label_var = ctk.StringVar(value=display_title)

        if environment == "Kültéri tevékenység":
            icon = h.OUTDOORS
        elif environment == "Beltéri tevékenység":
            icon = h.INDOORS
        else:
            icon = h.INDOORS

        if priority == "Alacsony":
            priority_icon = h.PRIORITY_ICON_1
        elif priority == "Közepes":
            priority_icon = h.PRIORITY_ICON_2
        elif priority == "Magas":
            priority_icon = h.PRIORITY_ICON_3
        else:
            priority_icon = h.PRIORITY_ICON_1
        
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0, minsize=60)
        self.columnconfigure(4, weight=0, minsize=60)

        if icon:
            self.icon_label = ctk.CTkLabel(self, image=icon, text="", width=100)
            self.icon_label.grid(row=0, column=0, padx=10, pady=8, sticky="w", rowspan=2)

        if priority_icon:
            self.priority_icon_label = ctk.CTkLabel(self, image=priority_icon, text="", width=100)
            self.priority_icon_label.grid(row=0, column=2, sticky="e", padx=(5,8), pady=(12,0))

        self.title_label = ctk.CTkLabel(self, textvariable=self.title_label_var, font=("Montserrat", 18, "bold"), width=280, wraplength=280, anchor="w")
        self.title_label.grid(row=0, column=1, padx=5, pady=(12,0))

        self.location_label = ctk.CTkLabel(self, text="Budapest", font=("Montserrat", 12))
        self.location_label.grid(row=1, column=1, padx=5, pady=(0,8), sticky="w")

        self.date_label = ctk.CTkLabel(self, text="nov. 18", font=("Montserrat", 12), width=100)
        self.date_label.grid(row=1, column=2, padx=5, pady=(0,8), sticky="e")

        refresh = h.REFRRSH
        self.edit_button = ctk.CTkButton(self, text="", image=refresh, command=lambda: self.undone(task_id), width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.edit_button.grid(row=0, column=3, padx=(0, 8), pady=8, sticky="nesw", rowspan=2)

        trash = h.TRASH
        self.trash_button = ctk.CTkButton(self, text="", image=trash, command=lambda: self.delete(task_id), width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.trash_button.grid(row=0, column=4, padx=(0, 8), pady=8, sticky="nesw", rowspan=2)



class ArchivedCollabTaskCard(ctk.CTkFrame):
    def __init__(self, parent, title, environment, priority, task_id, undone, delete, remove_from_collab, *args, **kwargs):
        super().__init__(parent, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.LIGHT_PURPLE, *args, **kwargs)
        
        self.undone = undone
        self.delete = delete
        self.task_id = task_id
        self.remove_from_collab = remove_from_collab

        self.db_helper = DatabaseHelper()

        self.is_creator = self.db_helper.is_creator(self.task_id)

        max_length = 20
        if len(title) > max_length:
            display_title = title[:max_length] + "..."
        else:
            display_title = title

        self.title_label_var = ctk.StringVar(value=display_title)

        if environment == "Kültéri tevékenység":
            icon = h.OUTDOORS
        elif environment == "Beltéri tevékenység":
            icon = h.INDOORS
        else:
            icon = h.INDOORS

        if priority == "Alacsony":
            priority_icon = h.PRIORITY_ICON_1
        elif priority == "Közepes":
            priority_icon = h.PRIORITY_ICON_2
        elif priority == "Magas":
            priority_icon = h.PRIORITY_ICON_3
        else:
            priority_icon = h.PRIORITY_ICON_1
        
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0, minsize=60)
        self.columnconfigure(4, weight=0, minsize=60)

        if icon:
            self.icon_label = ctk.CTkLabel(self, image=icon, text="", width=100)
            self.icon_label.grid(row=0, column=0, padx=10, pady=8, sticky="w", rowspan=2)

        if priority_icon:
            self.priority_icon_label = ctk.CTkLabel(self, image=priority_icon, text="", width=100)
            self.priority_icon_label.grid(row=0, column=2, sticky="e", padx=(5,8), pady=(12,0))

        self.title_label = ctk.CTkLabel(self, textvariable=self.title_label_var, font=("Montserrat", 18, "bold"), width=280, wraplength=280, anchor="w")
        self.title_label.grid(row=0, column=1, padx=5, pady=(12,0))

        self.location_label = ctk.CTkLabel(self, text="Budapest", font=("Montserrat", 12))
        self.location_label.grid(row=1, column=1, padx=5, pady=(0,8), sticky="w")

        self.date_label = ctk.CTkLabel(self, text="nov. 18", font=("Montserrat", 12), width=100)
        self.date_label.grid(row=1, column=2, padx=5, pady=(0,8), sticky="e")

        if self.is_creator:
            refresh = h.REFRRSH
            self.edit_button = ctk.CTkButton(self, text="", image=refresh, command=lambda: self.undone(task_id), width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE)
            self.edit_button.grid(row=0, column=3, padx=(0, 8), pady=8, sticky="nesw", rowspan=2)

            trash = h.TRASH
            self.trash_button = ctk.CTkButton(self, text="", image=trash, command=lambda: self.delete(task_id), width=60, bg_color=h.LIGHT_PURPLE, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE)
            self.trash_button.grid(row=0, column=4, padx=(0, 8), pady=8, sticky="nesw", rowspan=2)
        else:
            trash = h.TRASH
            self.trash_button = ctk.CTkButton(self, text="", image=trash, command=lambda: self.remove_from_collab(task_id), width=130, bg_color=h.LIGHT_PURPLE, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE)
            self.trash_button.grid(row=0, column=3, padx=(0, 8), pady=8, sticky="nesw", rowspan=2, columnspan=2)