import customtkinter as ctk
import header as h
import session
import database_helper as dbh
from frames.friend_card import FriendCard, RequestCard
from frames.task_card import ArchivedTaskCard, ArchivedCollabTaskCard
from frames.task_list_frame import TaskListFrame
from tkinter import messagebox

import bcrypt


def bind_button_events(button):
    def on_hover(event):
        button.configure(text_color=h.GREY_TEXT, fg_color=h.PALE_PURPLE)

    def off_hover(event):
        button.configure(text_color="white", fg_color=h.VIVID_PURPLE)

    def on_button_press(event):
        button.configure(fg_color=h.LIGHT_PURPLE)

    def on_button_release(event):
        button.configure(fg_color=h.VIVID_PURPLE)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", off_hover)
    button.bind("<ButtonPress>", on_button_press)
    button.bind("<ButtonRelease>", on_button_release)


class ArchivedTasksFrame(ctk.CTkToplevel):
    def __init__(self, parent, task_list_frame, main_frame_command, *args, **kwargs):
        super().__init__(parent, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)
        
        self.geometry("560x700")
        self.title("Archivált feladatok")
        self.resizable(False, False)
        self.grab_set()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (560 // 2)
        y = (screen_height // 2) - (700 // 2)

        self.geometry(f"+{x}+{y}")

        self.db_helper = dbh.DatabaseHelper()
        self.task_list_frame = task_list_frame
        self.main_frame_command = main_frame_command
        
        self.archived_tasks = self.db_helper.get_all_done_tasks()
        self.archived_collab_tasks = self.db_helper.get_all_done_collab_tasks()

        self.rowconfigure(0, weight=0, minsize=60)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(self, text="Archivált feladatok", font=("Montserrat", 24, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.name_label.grid(row=0, column=0, padx=16, pady=0, columnspan=2, sticky="w")

        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND)
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(0, weight=1)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew")

        self.refresh_done_tasks(self.archived_tasks, self.archived_collab_tasks)

    def display_tasks(self, tasks, collab_tasks):
        if collab_tasks:
            for index, task in enumerate(collab_tasks):
                task_title = task[2]
                task_priority = task[6]
                task_environment = task[7]
                task_id = task[0]
                task_card = ArchivedCollabTaskCard(self.scrollable_frame, title=task_title, priority=task_priority, environment=task_environment, task_id=task_id, undone=self.undone_task, delete=self.delete_archived_task, remove_from_collab=self.remove_from_archived_collab)
                task_card.grid(row=index, column=0, padx=5, pady=(0,10), sticky="nsew")
        if tasks:
            startfrom = len(collab_tasks)
            for index, task in enumerate(tasks):
                task_title = task[2]
                task_priority = task[6]
                task_environment = task[7]
                task_id = task[0]
                task_card = ArchivedTaskCard(self.scrollable_frame, title=task_title, priority=task_priority, environment=task_environment, task_id=task_id, undone=self.undone_task, delete=self.delete_archived_task)
                task_card.grid(row=index+startfrom, column=0, padx=5, pady=(0,10), sticky="nsew")

    def refresh_done_tasks(self, tasks, collab_tasks=[]):
        for widget in self.scrollable_frame.winfo_children():
            widget.grid_forget()
        
        self.display_tasks(tasks, collab_tasks)
    
    def undone_task(self, current_task_id):
        self.db_helper.task_undone(current_task_id)
        self.db_helper.revoke_points(current_task_id)
        self.main_frame_command()

        for widget in self.scrollable_frame.winfo_children():
            widget.grid_forget()
        
        self.display_tasks(self.db_helper.get_all_done_tasks(), self.db_helper.get_all_done_collab_tasks())

    def delete_archived_task(self, current_task_id):
        self.db_helper.delete_task(current_task_id)
        for widget in self.scrollable_frame.winfo_children():
            widget.grid_forget()
        
        self.display_tasks(self.db_helper.get_all_done_tasks(), self.db_helper.get_all_done_collab_tasks())

    def remove_from_archived_collab(self, task_id):
        self.db_helper.remove_from_collab(task_id)
        
        for widget in self.scrollable_frame.winfo_children():
            widget.grid_forget()
        
        self.display_tasks(self.db_helper.get_all_done_tasks(), self.db_helper.get_all_done_collab_tasks())

class AddFriendTopFrame(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)
        
        self.geometry("420x240")
        self.title("Barát hozzáadása")
        self.resizable(False, False)
        self.grab_set()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (420 // 2)
        y = (screen_height // 2) - (240 // 2)

        self.geometry(f"+{x}+{y}")

        self.rowconfigure(0, weight=0, minsize=60)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(self, text="Barát hozzáadása", font=("Montserrat", 24, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.name_label.grid(row=0, column=0, padx=16, pady=8, sticky="w")
        
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Barát email címe...", font=("Montserrat", 16), text_color=h.GREY_TEXT, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.email_entry.grid(row=1, column=0, sticky="nesw", padx=16, pady=8)

        self.send_request_button = ctk.CTkButton(self, text="Küldés", command=self.send_request, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
        self.send_request_button.grid(row=2, column=0, padx=16, pady=8, sticky="nesw")


    def send_request(self):
        if session.current_user_id is not None:
            friend_email = self.email_entry.get()
            
            self.db_helper = dbh.DatabaseHelper()
            check_if_exist = self.db_helper.send_friend_request(session.current_user_id, friend_email)
            if check_if_exist == False:
                messagebox.showwarning(title="Hiba", message="Nem létezik felhasználó ezzel az email címmel.")
            self.destroy()


class ProfileEditorTopFrame(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, fg_color=h.COLOR_BACKGROUND, *args, **kwargs)
        
        self.geometry("500x320")
        self.title("Jelszó megváltoztatása")
        self.resizable(False, False)
        self.grab_set()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (500 // 2)

        self.geometry(f"+{x}+{y}")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(4, weight=0, minsize=80)

        self.name_label = ctk.CTkLabel(self, text="Jelszóváltoztatás", font=("Montserrat", 24, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.name_label.grid(row=0, column=0, padx=16, pady=8, sticky="w", columnspan=2)
        
        self.old_pass_label = ctk.CTkLabel(self, text="Régi jelszó:", font=("Montserrat", 16, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.old_pass_label.grid(row=1, column=0, pady=(8, 4), padx=(16, 8), sticky="w")
        
        self.old_pass = ctk.CTkEntry(self, font=("Montserrat", 16), text_color=h.GREY_TEXT, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, show="*")
        self.old_pass.grid(row=1, column=1, pady=(8, 4), padx=(8, 16), sticky="nesw")

        self.new_pass_label = ctk.CTkLabel(self, text="Új jelszó:", font=("Montserrat", 16, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.new_pass_label.grid(row=2, column=0, pady=4, padx=(16, 8), sticky="w")
        
        self.new_pass = ctk.CTkEntry(self, font=("Montserrat", 16), text_color=h.GREY_TEXT, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, show="*")
        self.new_pass.grid(row=2, column=1, pady=4, padx=(8, 16), sticky="nesw")

        self.new_pass_again_label = ctk.CTkLabel(self, text="Új jelszó megismétlése:", font=("Montserrat", 16, "bold"), bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.new_pass_again_label.grid(row=3, column=0, pady=(4, 8), padx=(16, 8), sticky="w")
        
        self.new_pass_again = ctk.CTkEntry(self, font=("Montserrat", 16), text_color=h.GREY_TEXT, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND, show="*")
        self.new_pass_again.grid(row=3, column=1, pady=(4, 8), padx=(8, 16), sticky="nesw")

        self.save_button = ctk.CTkButton(self, text="Mentés", command=self.save_data, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
        self.save_button.grid(row=4, column=0, padx=16, pady=8, sticky="nesw")

        self.cancel_button = ctk.CTkButton(self, text="Mégse", command=self.destroy, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
        self.cancel_button.grid(row=4, column=1, padx=16, pady=8, sticky="nesw")

    def save_data(self):
        if session.current_user_id != None:
            self.user_data = session.get_current_user_data(session.current_user_id)

            old_pass = self.old_pass.get()
            new_pass = self.new_pass.get()
            new_pass_again = self.new_pass_again.get()

            if bcrypt.checkpw(old_pass.encode('utf-8'), self.user_data.password.encode('utf-8')):
                if new_pass == new_pass_again:
                    try:
                        self.db_helper = dbh.DatabaseHelper()
                        self.db_helper.update_password(self.user_data.user_id, new_pass)
                        
                    except Exception as e:
                       print(f"exception: {e}")
                else:
                    print("message box ohgy nem jo a ketto")
            else:
                print("regi jelszo nem jo message")
        
        self.destroy()

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback, main_frame_command, *args, **kwargs):
        super().__init__(parent, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND,*args, **kwargs)

        self.main_frame_command = main_frame_command
        self.db_helper = dbh.DatabaseHelper()
        self.navigate_callback = navigate_callback
        self.friends = self.db_helper.get_friends(session.current_user_id)
        self.requests = self.db_helper.get_requests(session.current_user_id)

        self.rowconfigure(0, weight=0, minsize=60)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0, minsize=80)
        self.rowconfigure(3, weight=0, minsize=80)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        if session.current_user_id != None:
            self.user_data = session.get_current_user_data(session.current_user_id)

            self.name_label = ctk.CTkLabel(self, text="Barátok", font=("Montserrat", 24, "bold"))
            self.name_label.grid(row=0, column=0, padx=16, pady=0, columnspan=2, sticky="w")

            self.parent_friends_frame = ctk.CTkFrame(self, corner_radius=10, border_color=h.PALE_PURPLE, border_width=5, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
            self.parent_friends_frame.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=12, pady=(0,12))
            self.parent_friends_frame.rowconfigure(0, weight=1)
            self.parent_friends_frame.rowconfigure(1, weight=0, minsize=60)
            self.parent_friends_frame.columnconfigure(0, weight=1)

            self.add_friends_button = ctk.CTkButton(self.parent_friends_frame, text="+ Új barát hozzáadása", command=self.open_add_friend_topframe, font=("Montserrat", 16), height=60, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
            self.add_friends_button.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew")

            self.friends_frame = ctk.CTkScrollableFrame(self.parent_friends_frame, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
            self.friends_frame.columnconfigure(0, weight=1)
            self.friends_frame.rowconfigure(0, weight=1)
            self.friends_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            self.friends_frame_none = ctk.CTkFrame(self.parent_friends_frame, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
            self.friends_frame_none.columnconfigure(0, weight=1)
            self.friends_frame_none.rowconfigure(0, weight=1)
            self.friends_frame_none.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            self.no_friends_label = ctk.CTkLabel(self.friends_frame_none, text="Nincsenek még barátaid.", font=("Montserrat", 24, "bold"))
            self.no_friends_label.grid(row=0, column=0, sticky="nesw")

            if len(self.friends) != 0:
                self.friends_frame_none.grid_forget()
                self.no_friends_label.grid_forget()
            else:
                self.friends_frame.grid_forget()

            self.profile_edit_button = ctk.CTkButton(self, text="Jelszóváltoztatás", command=self.open_profile_editor, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
            self.profile_edit_button.grid(row=2, column=0, padx=(10, 5), pady=(0,10), sticky="nsew")

            
            self.archive_button = ctk.CTkButton(self, text="Archivált feladatok", command=self.open_archived_topframe, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
            self.archive_button.grid(row=2, column=1, padx=(5, 10), pady=(0,10), sticky="nsew")

            if len(self.db_helper.get_all_done_collab_tasks()) == 0 and len(self.db_helper.get_all_done_tasks()) == 0:
                self.archive_button.configure(state="disabled")
            else:
                self.archive_button.configure(state="normal")

            self.logout_button = ctk.CTkButton(self, text="Kijelentkezés", command=self.logout_process, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
            self.logout_button.grid(row=3, column=0, padx=10, pady=(0,10), sticky="nsew", columnspan=2)

            self.refresh_requests(self.requests)

            self.refresh_friends(self.friends)

            bind_button_events(self.add_friends_button)
            bind_button_events(self.profile_edit_button)
            bind_button_events(self.archive_button)
            bind_button_events(self.logout_button)

    def refresh_requests(self, requests):
        for widget in self.friends_frame.winfo_children():
            widget.grid_forget()

        self.display_requests(requests)

    def display_requests(self, requests):
        self.reqs = ctk.CTkLabel(self.friends_frame, text="Bejövő felkérések", font=("Montserrat", 18, "bold"))
        self.reqs.grid(row=0, column=0, sticky="w", padx=12, pady=8)
        self.line = ctk.CTkFrame(self.friends_frame, height=5, fg_color=h.LIGHT_PURPLE)
        if len(requests) != 0:
            self.friends_frame_none.grid_forget()
            self.no_friends_label.grid_forget()
            self.friends_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.db_helper = dbh.DatabaseHelper()
            for index, request in enumerate(requests):

                if request != None:
                    friend_id = request[0]
                    friend_email = request[1]
                    friend_points = request[2]

                    request_card = RequestCard(self.friends_frame, friend_id=friend_id, email=friend_email, points=friend_points, accept=self.accpet_request, deny=self.deny_request)
                    request_card.grid(row=index+1, column=0, padx=5, pady=(0,10), sticky="nsew")

            self.line = ctk.CTkFrame(self.friends_frame, height=5, fg_color=h.LIGHT_PURPLE)
            self.line.grid(row=(len(requests)+2), column=0, sticky="nsew", padx=20, pady=(10,20))
        else:
            self.reqs.grid_forget()
            self.line.grid_forget()


    def refresh_friends(self, friends):
        for widget in self.friends_frame.winfo_children():
            if isinstance(widget, FriendCard):
                widget.grid_forget()

        self.display_friends(friends)

    def display_friends(self, friends):
        self.start_from = 0
        if len(friends) != 0:
            if self.requests != 0:
                self.start_from = len(self.requests)+3
            else:
                self.start_from = 0
            self.friends_frame_none.grid_forget()
            self.no_friends_label.grid_forget()
            self.friends_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.db_helper = dbh.DatabaseHelper()
            for index, friend in enumerate(friends):
                friend_data = self.db_helper.get_friend_data(friend[0])
                if friend_data != None:
                    friend_id = friend_data[0][0]
                    friend_email = friend_data[0][3]
                    friend_points = friend_data[0][5]

                    friend_card = FriendCard(self.friends_frame, friend_id=friend_id, email=friend_email, points=friend_points, unfriend=self.unfriend)
                    friend_card.grid(row=(self.start_from+index), column=0, padx=5, pady=(0,10), sticky="nsew")
        else:
            if len(self.requests) != 0:
                self.friends_frame_none.grid_forget()
                self.no_friends_label.grid_forget()
            else:
                self.friends_frame.grid_forget()
                self.friends_frame_none.grid(row=self.start_from, column=0, sticky="nsew", padx=10, pady=10)
                self.no_friends_label.grid(row=0, column=0, sticky="nesw")
            
    


    def open_profile_editor(self):
        ProfileEditorTopFrame(self)

    def open_add_friend_topframe(self):
        AddFriendTopFrame(self)

    def open_archived_topframe(self):
        ArchivedTasksFrame(self, TaskListFrame, self.main_frame_command)

    def unfriend(self, friend_id):
        print(f"friend id torleshez : {friend_id}")
        response = messagebox.askyesno('Barátság törlése','Biztos hogy törölni kívánja a barátságot?')
        if response:
            self.db_helper.unfriend(friend_id)

            friends = self.db_helper.get_friends(session.current_user_id)
            self.refresh_friends(friends)

        else:
            return
        
    def logout_process(self):
        session.logout()
        self.db_helper.close_connection()
        self.navigate_callback("login") 

    
    def accpet_request(self, friend_id):
        self.db_helper.accept_friend_request(friend_id)
        self.refresh_requests(self.db_helper.get_requests(session.current_user_id))
        self.refresh_friends(self.db_helper.get_friends(session.current_user_id))

    def deny_request(self, friend_id):
        self.db_helper.deny_friend_request(friend_id)
        self.refresh_requests(self.db_helper.get_requests(session.current_user_id))
        self.refresh_friends(self.db_helper.get_friends(session.current_user_id))