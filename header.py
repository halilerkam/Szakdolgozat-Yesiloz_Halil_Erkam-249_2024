from PIL import Image
import customtkinter as ctk
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 900
PADDING_X = 40
PADDING_Y = 60
PADDING_X_BOTH_SIDES = 80

# Színek
SOFT_WHITE = "#F9F9F9" #Soft White (background, text)
COLOR_BACKGROUND = "#F7F7F7" #Light Grey (secondary backgrounds)
MEDIUM_GREY = "#D1D1D1" #Medium Grey (subtle text or dividers)
VIVID_PURPLE = "#9B4DFF" #Vivid Purple (primary accent, buttons)
PALE_PURPLE = "#D1A8FF" #Pale Purple (hover, soft highlights)
LIGHT_PURPLE = "#E6C8FF" #Light Purple (backgrounds, soft sections)
GREY_TEXT = "#333" #dark grey like logo text


#ikonok
MAIN_LOGO_SIZE = (600, 120)
MAIN_LOGO_PATH = os.path.join(BASE_PATH, "icons/main_logo.png")
MAIN_LOGO = ctk.CTkImage(Image.open(MAIN_LOGO_PATH), size=MAIN_LOGO_SIZE)

LOGO_ICON_SIZE = (60, 60)
LOGO_ICON_PATH = os.path.join(BASE_PATH, "icons/logo_icon.png")
LOGO_ICON = ctk.CTkImage(Image.open(LOGO_ICON_PATH), size=LOGO_ICON_SIZE)

FAVICON = os.path.join(BASE_PATH, "icons/logo_favicon.ico")

INDOORS_SIZE = (30, 30)
INDOORS = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/indoors.png")), size=INDOORS_SIZE)

OUTDOORS_SIZE = (30, 30)
OUTDOORS = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/outdoors.png")), size=OUTDOORS_SIZE)

ICON_SIZE = (60, 20)
PRIORITY_ICON_1 = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/priority_icon_1.png")), size=ICON_SIZE)
PRIORITY_ICON_2 = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/priority_icon_2.png")), size=ICON_SIZE)
PRIORITY_ICON_3 = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/priority_icon_3.png")), size=ICON_SIZE)

LOGO_SYMBOL_SIZE = (60, 60)
LOGO_SYMBOL = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/logo_symbol.png")), size=LOGO_SYMBOL_SIZE)

PROFILE_SIZE = (35, 35)
PROFILE = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/profile_icon_1_purple.png")), size=PROFILE_SIZE)

ARROW_RIGHT_SIZE = (30, 30)
ARROW_RIGHT = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/arrow_to_right.png")), size=ARROW_RIGHT_SIZE)

ARROW_LEFT_SIZE = (30, 30)
ARROW_LEFT = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/arrow_to_left.png")), size=ARROW_LEFT_SIZE)

CHECK_SIZE = (30, 30)
CHECK = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/check.png")), size=CHECK_SIZE)

CALENDAR_SIZE = (30, 30)
CALENDAR_ICON = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/calendar_1.png")), size=CALENDAR_SIZE)

COLLAB_STARS_SIZE = (30, 30)
COLLAB_STARS = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/collab_stars_3.png")), size=COLLAB_STARS_SIZE)

REFRESH_SIZE = (30, 30)
REFRRSH = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/REFRESH_2.png")), size=REFRESH_SIZE)

TRASH_SIZE = (30, 30)
TRASH = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/trash.png")), size=TRASH_SIZE)

ADD_FRIEND_SIZE = (30, 30)
ADD_FRIEND = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/add_friend.png")), size=ADD_FRIEND_SIZE)

USER_DELETE_SIZE = (30, 30)
USER_DELETE = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/user_delete.png")), size=USER_DELETE_SIZE)

ACCEPT_SIZE = (30, 30)
ACCEPT = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/accept.png")), size=ACCEPT_SIZE)

DENY_SIZE = (30, 30)
DENY = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/deny.png")), size=DENY_SIZE)

WEATHER_ALERT_SIZE = (25, 25)
WEATHER_ALERT = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/weather_alert.png")), size=WEATHER_ALERT_SIZE)

ADD_SIZE = (30, 30)
ADD = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/add.png")), size=ADD_SIZE)

REMOVE_SIZE = (30, 30)
REMOVE = ctk.CTkImage(Image.open(os.path.join(BASE_PATH, "icons/remove.png")), size=REMOVE_SIZE)