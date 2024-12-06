import customtkinter as ctk
import header as h
from database_helper import DatabaseHelper

class FriendCard(ctk.CTkFrame):
    def __init__(self, parent, friend_id, email, points, unfriend, *args, **kwargs):
        super().__init__(parent, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)

        self.friend_id = friend_id
        self.email = email
        self.points = points
        self.unfriend = unfriend
        
        self.rowconfigure(0, weight=3)  # top row
        self.columnconfigure(0, weight=3) #left column
        self.columnconfigure(1, weight=1) #mid left column
        self.columnconfigure(2, weight=0, minsize=60) #mid right column

        self.friend_email_label = ctk.CTkLabel(self, text=self.email, font=("Montserrat", 16, "bold"), height=60)
        self.friend_email_label.grid(row=0, column=0, padx=16, pady=8, sticky="w")

        collab_stars = h.COLLAB_STARS
        self.friend_points_label = ctk.CTkLabel(self, text=f"  {self.points}", font=("Montserrat", 16, "bold"), image=collab_stars, anchor="e", compound="left", width=60, height=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.friend_points_label.grid(row=0, column=1, padx=(5,10), pady=8, sticky="nesw")

        """ trash = h.TRASH
        self.delete_button =ctk.CTkButton(self, text="", image=trash, width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.PALE_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.delete_button.grid(row=0, column=2, pady=8, padx=(0,8), sticky="nesw", rowspan=2) """

        user_delete = h.USER_DELETE
        self.delete_button =ctk.CTkButton(self, text="", image=user_delete, command=lambda: self.unfriend(friend_id), width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.PALE_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.delete_button.grid(row=0, column=2, pady=8, padx=8, sticky="nesw", rowspan=2)


class RequestCard(ctk.CTkFrame):
    def __init__(self, parent, friend_id, email, points, accept, deny, *args, **kwargs):
        super().__init__(parent, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.PALE_PURPLE, *args, **kwargs)

        self.friend_id = friend_id
        self.email = email
        self.points = points
        self.accept = accept
        self.deny = deny
        
        self.rowconfigure(0, weight=3)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0, minsize=60)
        self.columnconfigure(3, weight=0, minsize=60)

        self.friend_email_label = ctk.CTkLabel(self, text=self.email, font=("Montserrat", 16, "bold"), height=60, bg_color=h.PALE_PURPLE, fg_color=h.PALE_PURPLE)
        self.friend_email_label.grid(row=0, column=0, padx=16, pady=8, sticky="w")

        collab_stars = h.COLLAB_STARS
        self.friend_points_label = ctk.CTkLabel(self, text=f"  {self.points}", font=("Montserrat", 16, "bold"), image=collab_stars, anchor="e", compound="left", width=60, height=60, bg_color=h.PALE_PURPLE, fg_color=h.PALE_PURPLE)
        self.friend_points_label.grid(row=0, column=1, padx=(5,10), pady=8, sticky="nesw")

        deny_logo = h.DENY
        self.deny_button = ctk.CTkButton(self, text="", command=lambda: self.deny(friend_id), image=deny_logo, width=60, bg_color=h.PALE_PURPLE, fg_color=h.SOFT_WHITE, hover_color=h.LIGHT_PURPLE)
        self.deny_button.grid(row=0, column=2, padx=(0, 8), pady=8, sticky="nesw")

        accept_logo = h.ACCEPT
        self.accept_button = ctk.CTkButton(self, text="", command=lambda: self.accept(friend_id), image=accept_logo, width=60, bg_color=h.PALE_PURPLE, fg_color=h.VIVID_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.accept_button.grid(row=0, column=3, padx=(0, 8), pady=8, sticky="nesw")

class FriendsCheckbox(ctk.CTkFrame):
    def __init__(self, parent, friend_id, email, points, callback, toggled, *args, **kwargs):
        super().__init__(parent, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)

        self.friend_id = friend_id
        self.email = email
        self.points = points
        self.callback = callback
        self.toggled = toggled
        
        self.rowconfigure(0, weight=3)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0, minsize=60)
        self.columnconfigure(3, weight=0, minsize=60)

        self.friend_email_label = ctk.CTkLabel(self, text=self.email, font=("Montserrat", 16, "bold"), height=60)
        self.friend_email_label.grid(row=0, column=0, padx=16, pady=8, sticky="w")

        collab_stars = h.COLLAB_STARS
        self.friend_points_label = ctk.CTkLabel(self, text=f"  {self.points}", font=("Montserrat", 16, "bold"), image=collab_stars, anchor="e", compound="left", width=60, height=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.friend_points_label.grid(row=0, column=1, padx=(5,10), pady=8, sticky="nesw")

        self.switch = ctk.CTkSwitch(self, text="", fg_color=h.COLOR_BACKGROUND, command=lambda: self.toggle_fg_color())
        self.switch.grid(row=0, column=3, pady=8, padx=8, sticky="nesw", rowspan=2)

        self.add = h.ADD
        self.remove = h.REMOVE
        self.toggle_button =ctk.CTkButton(self, text="", image=self.add, command=self.switch_button, width=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.PALE_PURPLE, hover_color=h.LIGHT_PURPLE)
        self.toggle_button.grid(row=0, column=3, pady=8, padx=8, sticky="nesw", rowspan=2)

        if(toggled):
            self.switch.select()
            self.configure(fg_color=h.LIGHT_PURPLE)
            self.friend_points_label.configure(fg_color=h.LIGHT_PURPLE)
            self.toggle_button.configure(fg_color=h.PALE_PURPLE)
            self.toggle_button.configure(image=self.remove)
        else:
            self.switch.deselect()
            self.configure(fg_color=h.COLOR_BACKGROUND)
            self.friend_points_label.configure(fg_color=h.COLOR_BACKGROUND)
            self.toggle_button.configure(fg_color=h.LIGHT_PURPLE)
            self.toggle_button.configure(image=self.add)

    def toggle_fg_color(self):
        if self.switch.get() == 0:
            self.configure(fg_color=h.COLOR_BACKGROUND)
            self.friend_points_label.configure(fg_color=h.COLOR_BACKGROUND)
            self.toggle_button.configure(fg_color=h.LIGHT_PURPLE)
            self.toggle_button.configure(image=self.add)
        else:
            self.configure(fg_color=h.LIGHT_PURPLE)
            self.friend_points_label.configure(fg_color=h.LIGHT_PURPLE)
            self.toggle_button.configure(fg_color=h.PALE_PURPLE)
            self.toggle_button.configure(image=self.remove)

    def switch_button(self):
        self.switch.toggle()
        if self.callback:
            self.callback(self.friend_id)

    def check_selection_limit(self, selected_list):
        selected_count = len(selected_list)
        if selected_count <= self.max_selections:
            selected_list.append(self.friend_id)

    