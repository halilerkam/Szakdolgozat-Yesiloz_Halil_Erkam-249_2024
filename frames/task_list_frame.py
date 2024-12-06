import customtkinter as ctk
from frames.task_card import TaskCard, CollabTaskCard
import header as h
import session
from database_helper import DatabaseHelper
from weather_api import WeatherAPI
import datetime


class TaskListFrame(ctk.CTkFrame):
    def __init__(self, parent, navigate_inside, navigate_to_edit_task, db_helper, has_change, *args, **kwargs):
        super().__init__(parent, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND, *args, **kwargs)

        self.navigate_inside = navigate_inside
        self.navigate_to_edit_task = navigate_to_edit_task
        self.db_helper = db_helper

        self.weather_data = []

        self.weather_api = WeatherAPI(api_key="5556a2ce21fb6b88d2a580bc7a0d38c7")

        self.check_weather()
        self.start_weather_update_timer()
        
        self.okay_weathers = ["clear sky", "few clouds", "scattered clouds", "broken clouds", "overcast clouds"]
        self.alerting = None

        self.has_changed = has_change

        self.tasks = self.db_helper.get_all_tasks()
        self.collab_tasks = self.db_helper.get_collab_tasks()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0, minsize=50)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=h.COLOR_BACKGROUND, bg_color=h.COLOR_BACKGROUND)
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(0, weight=1)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")

        self.tasks_frame_none = ctk.CTkFrame(self, bg_color=h.COLOR_BACKGROUND, fg_color=h.COLOR_BACKGROUND)
        self.tasks_frame_none.columnconfigure(0, weight=1)
        self.tasks_frame_none.rowconfigure(0, weight=1)
        self.tasks_frame_none.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.no_tasks_label = ctk.CTkLabel(self.tasks_frame_none, text="Nincsenek még feladataid.", font=("Montserrat", 24, "bold"))
        self.no_tasks_label.grid(row=0, column=0, sticky="nesw")

        
        if self.tasks != None:
            self.tasks_frame_none.grid_forget()
            self.no_tasks_label.grid_forget()
            self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.scrollable_frame.grid_forget()
            self.tasks_frame_none.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.no_tasks_label.grid(row=0, column=0, sticky="nesw")

        self.add_content_button = ctk.CTkButton(self, text="+ Feladat hozzaadasa", command=lambda: self.navigate_inside("add_task"), font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
        self.add_content_button.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew")

        """ self.weather_button = ctk.CTkButton(self, text="Időjárás ellenőrzése", command=self.check_weather)
        self.weather_button.grid(row=1, column=2, padx=10, pady=(0,10), sticky="nsew") """

        """ self.add_content_button2 = ctk.CTkButton(self, text="update view", command=self.update_view, font=("Montserrat", 16), height=80, bg_color=h.COLOR_BACKGROUND, fg_color=h.VIVID_PURPLE)
        self.add_content_button2.grid(row=2, column=0, padx=10, pady=(0,10), sticky="nsew") """

        def on_hover(event):
            self.add_content_button.configure(text_color=h.GREY_TEXT, fg_color=h.PALE_PURPLE)
        def off_hover(event):
            self.add_content_button.configure(text_color="white", fg_color=h.VIVID_PURPLE)

        def on_button_press(event):
            # Szín módosítása nyomás alatt
            self.add_content_button.configure(fg_color=h.LIGHT_PURPLE)

        def on_button_release(event):
            # Szín visszaállítása az eredetire
            self.add_content_button.configure(fg_color=h.VIVID_PURPLE)

        self.add_content_button.bind("<Enter>", on_hover)  # Amikor az egér a gomb fölé kerül
        self.add_content_button.bind("<Leave>", off_hover)  # Amikor az egér elhagyja a gombot
        self.add_content_button.bind("<ButtonPress>", on_button_press)
        self.add_content_button.bind("<ButtonRelease>", on_button_release)

        if session.current_user_id != None:
            self.refresh_tasks(self.tasks, self.collab_tasks)

    def check_weather(self, task_id=None):
        if session.current_user_id:
            city_date_pairs = self.db_helper.get_city_date_pairs()

            for pair in city_date_pairs:
                if task_id == None:
                    id = pair['id']
                    city_name = pair["city"]
                    target_date = pair["date"]

                    latitude, longitude = self.weather_api.get_coordinates(city_name)
                    if latitude is None or longitude is None:
                        print(f"Érvénytelen város: {city_name} - kihagyásra került.")
                        continue

                    forecast = self.weather_api.fetch_daily_forecast(latitude, longitude)
                    print(forecast)
                    if forecast:
                        matched_day = next((day for day in forecast if day["date"] == str(target_date)), None)
                        if matched_day:
                            print(f"Időjárás jelentés {city_name} számára {target_date}:")
                            weather = matched_day["weather"]
                            min_temp = matched_day["min_temp"]
                            max_temp = matched_day["max_temp"]
                            print(matched_day)
                            self.weather_data.append({
                                "id": id,
                                "city": city_name,
                                "date": target_date,
                                "weather": matched_day["weather"]
                            })
                            print(f"{weather}, Min: {min_temp}°C, Max: {max_temp}°C")
                        else:
                            print(f"Nincs elérhető előrejelzés a(z) {target_date} dátumra {city_name} számára.")
                    else:
                        print(f"Nem sikerült lekérni az időjárás adatokat a(z) '{city_name}' városhoz.")
                elif task_id == pair['id']:
                    id = pair['id']
                    city_name = pair["city"]
                    target_date = pair["date"]

                    latitude, longitude = self.weather_api.get_coordinates(city_name)
                    if latitude is None or longitude is None:
                        print(f"Érvénytelen város: {city_name} - kihagyásra került.")
                        continue

                    forecast = self.weather_api.fetch_daily_forecast(latitude, longitude)
                    print(forecast)
                    if forecast:
                        matched_day = next((day for day in forecast if day["date"] == str(target_date)), None)
                        if matched_day:
                            print(f"Időjárás jelentés {city_name} számára {target_date}:")
                            weather = matched_day["weather"]
                            min_temp = matched_day["min_temp"]
                            max_temp = matched_day["max_temp"]
                            print(matched_day)
                            for i in self.weather_data:
                                if i['id'] == task_id:
                                    self.weather_data.remove(i)
                                    self.weather_data.append({
                                        "id": id,
                                        "city": city_name,
                                        "date": target_date,
                                        "weather": matched_day["weather"]
                                    })
                                    print(f"{weather}, Min: {min_temp}°C, Max: {max_temp}°C")
                        else:
                            print(f"Nincs elérhető előrejelzés a(z) {target_date} dátumra {city_name} számára.")
                    else:
                        print(f"Nem sikerült lekérni az időjárás adatokat a(z) '{city_name}' városhoz.")



    def start_weather_update_timer(self):
        six_hours_in_milliseconds = 6 * 60 * 60 * 1000  # 6 óra milliszekundumban
        self.master.after(six_hours_in_milliseconds, self.update_weather_timer)

    def update_weather_timer(self):
        print("6 órás időzítő aktiválva: időjárás frissítése...")
        self.check_weather()
        self.start_weather_update_timer()
        self.refresh_tasks(self.db_helper.get_all_tasks(), self.db_helper.get_collab_tasks())

    def navigate_to_edit(self, current_task_id):
        self.navigate_to_edit_task(current_task_id)
    
    def done_task(self, current_task_id):
        self.db_helper.task_done(current_task_id)
        self.db_helper.reward_points(current_task_id)
        self.refresh_tasks(self.db_helper.get_all_tasks(), self.db_helper.get_collab_tasks())        

    def refresh_tasks(self, tasks, collab_tasks=[]):
        for widget in self.scrollable_frame.winfo_children():
            widget.grid_forget()
        
        self.display_tasks(tasks, collab_tasks)

    def display_tasks(self, tasks, collab_tasks):
        if len(collab_tasks) != 0:
            self.tasks_frame_none.grid_forget()
            self.no_tasks_label.grid_forget()
            self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
            for index, task in enumerate(collab_tasks):
                self.alerting = None
                task_title = task[2]
                task_date = task[4]
                if task_date == None:
                    task_date = "Dátum: -"
                task_location = task[5]
                task_priority = task[6]
                task_environment = task[7]
                task_id = task[0]
                weather_info = next((data for data in self.weather_data if data["id"] == task_id), None)
                if weather_info:
                    weather_desc = weather_info["weather"]
                    if weather_desc not in self.okay_weathers:
                        self.alerting = weather_desc
                task_card = CollabTaskCard(self.scrollable_frame, title=task_title, priority=task_priority, environment=task_environment, task_id=task_id, task_date=task_date, task_location=task_location, alert=self.alerting, navigate=self.navigate_to_edit, done=self.done_task)
                task_card.grid(row=index, column=0, padx=5, pady=(0,10), sticky="nsew")
        else:
            self.scrollable_frame.grid_forget()
            self.tasks_frame_none.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.no_tasks_label.grid(row=0, column=0, sticky="nsew")
        
        if len(tasks) != 0:
            startfrom = len(collab_tasks)
            self.tasks_frame_none.grid_forget()
            self.no_tasks_label.grid_forget()
            self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
            for index, task in enumerate(tasks):
                self.alerting = None
                task_title = task[2]
                task_date = task[4]
                if task_date == None:
                    task_date = "Dátum: -"
                task_location = task[5]
                task_priority = task[6]
                task_environment = task[7]
                task_id = task[0]
                weather_info = next((data for data in self.weather_data if data["id"] == task_id), None)
                if weather_info:
                    weather_desc = weather_info["weather"]
                    if weather_desc not in self.okay_weathers:
                        self.alerting = weather_desc
                task_card = TaskCard(self.scrollable_frame, title=task_title, priority=task_priority, environment=task_environment, task_id=task_id, task_date=task_date, task_location=task_location, alert=self.alerting, navigate=self.navigate_to_edit, done=self.done_task)
                task_card.grid(row=index+startfrom, column=0, padx=5, pady=(0,10), sticky="nsew")
        elif len(tasks) == 0 and len(collab_tasks) == 0:
            self.scrollable_frame.grid_forget()
            self.tasks_frame_none.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.no_tasks_label.grid(row=0, column=0, sticky="nsew")
            
    
    