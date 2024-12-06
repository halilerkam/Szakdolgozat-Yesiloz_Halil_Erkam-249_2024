import customtkinter as ctk
from frames.login_frame import LoginFrame
from frames.register_frame import RegisterFrame
from frames.main_frame import MainFrame
import header as h

import database_helper

db_helper = database_helper.DatabaseHelper()


class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("TaskFlow")

        favicon = h.FAVICON
        self.iconbitmap(favicon)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 600
        window_height = 900

        position_top = (screen_height // 2) - (window_height // 2)
        position_right = (screen_width // 2) - (window_width // 2)

        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.resizable(False, False)

        self.frames = {
            "login": LoginFrame(self, self.on_login_success, self.navigate, db_helper=db_helper),
            "register": RegisterFrame(self, self.navigate, db_helper=db_helper),
            "main": MainFrame(self, self.navigate, db_helper, navigate_callback=self.navigate)
        }

        for frame in self.frames.values():
            frame.pack(fill="both", expand=True)
        self.navigate("login")
        
    
    def navigate(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()

        if frame_name == "main":
            self.frames["main"] = MainFrame(self, self.navigate, db_helper, navigate_callback=self.navigate)
            self.frames["main"].pack(fill="both", expand=True)
        elif frame_name == "login":
            self.frames["login"].pack(fill="both", expand=True)
        elif frame_name == "register":
            self.frames["register"].pack(fill="both", expand=True)
        else:
            self.frames[frame_name].pack(fill="both", expand=True)

    def on_login_success(self):
        self.navigate("main")
        
        
# Alkalmazás indítása
if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()