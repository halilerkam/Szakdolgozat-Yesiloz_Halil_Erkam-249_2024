import customtkinter as ctk
import session
import mysql.connector
from header import COLOR_BACKGROUND
from database_helper import has_changed


from frames.header_frame import HeaderFrame
from frames.profile_frame import ProfileFrame
from frames.task_list_frame import TaskListFrame
from frames.add_task_frame import AddTaskFrame
from frames.edit_task_frame import EditTaskFrame

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, navigate, db_helper, navigate_callback):
        super().__init__(parent, bg_color=COLOR_BACKGROUND, fg_color=COLOR_BACKGROUND)
        self.parent = parent
        self.navigate = navigate
        self.db_helper = db_helper
        self.navigate_callback = navigate_callback

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0, minsize=100)
        self.rowconfigure(1, weight=1)


        self.header_frame = HeaderFrame(self, title="Főoldal", navigate_callback=self.navigate_inside, height=100)
        self.header_frame.grid(row=0, column=0, sticky="nsew")

        self.task_list_frame = TaskListFrame(self, self.navigate_inside, self.navigate_to_edit_task, self.db_helper, has_changed)
        self.task_list_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10,0))
        
    def navigate_inside(self, frame_name):
        # Navigálás különböző framek között
        if frame_name == "profile":
            self.show_profile()
        elif frame_name == "main":
            self.show_main()
        elif frame_name == "main_w_warning":
            self.show_main_w_warning()
        elif frame_name == "add_task":
            self.show_add_task()
        elif frame_name == "edit_task":
            self.show_edit_task()
            
    def navigate_to_edit_task(self, current_task_id):
        if current_task_id != None:
            self.show_edit_task(current_task_id)

    def show_profile(self):
        self.task_list_frame.grid_forget()

        self.profile_frame = ProfileFrame(self, navigate_callback=self.navigate_callback, main_frame_command=self.update_points)
        self.profile_frame.grid(row=1, column=0, sticky="nesw")

        self.user_data = session.get_current_user_data(session.current_user_id)

        self.header_frame.update_title("Szia, " + self.user_data.first_name + "!")
        self.header_frame.update_back_button("main")
    
    def update_points(self):
        self.header_frame.collab_stars_icon.configure(text=self.db_helper.get_current_points())
    
    def show_add_task(self):
        self.task_list_frame.grid_forget()
        if hasattr(self, 'profile_frame'):
            self.profile_frame.grid_forget()

        self.header_frame.update_title("Új feladat hozzáadása")
        self.header_frame.update_back_button("main")
        self.header_frame.icon_label.grid_forget()
        self.header_frame.back_button.grid()
        self.header_frame.profile_button.grid_forget()

        self.add_task_frame = AddTaskFrame(self, task_list_frame=self.task_list_frame, db_helper=self.db_helper, navigate_callback=self.navigate_inside)
        self.add_task_frame.grid(row=1, column=0, sticky="nsew")

    def show_edit_task(self, task_id):
        self.task_list_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10,0))
        self.task_list_frame.grid_forget()
        if hasattr(self, 'profile_frame'):
            self.profile_frame.grid_forget()

        self.header_frame.update_title("Feladat részletei")
        self.header_frame.update_back_button("main_w_warning", "edit_task")
        self.header_frame.icon_label.grid_forget()
        self.header_frame.back_button.grid()
        self.header_frame.profile_button.grid_forget()

        self.edit_task_frame = EditTaskFrame(self, task_list_frame=self.task_list_frame, db_helper=self.db_helper, navigate_callback=self.navigate_inside, task_id=task_id)
        self.edit_task_frame.grid(row=1, column=0, sticky="nsew")


    def show_main(self, origin=None):
        if hasattr(self, "profile_frame"):
            self.profile_frame.grid_forget()
        if hasattr(self, "add_task_frame"):
            self.add_task_frame.grid_forget()
        if hasattr(self, "edit_task_frame"):
            self.edit_task_frame.grid_forget()
            
        self.task_list_frame.grid(row=1, column=0, sticky="nsew")
        self.header_frame.profile_button.grid(row=0, column=2, padx=(10, 24), sticky="e")

        self.header_frame.update_title("Feladatok")
        self.header_frame.update_back_button("")
        self.task_list_frame.refresh_tasks(self.db_helper.get_all_tasks(), self.db_helper.get_collab_tasks())
        

    def show_main_w_warning(self):
        if hasattr(self, "edit_task_frame"):
            if self.edit_task_frame.edit_task_back():
                self.header_frame.update_title("Feladatok")
                self.header_frame.update_back_button("")
        