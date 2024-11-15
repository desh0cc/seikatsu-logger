import flet as ft, json, os
from datetime import datetime

from libs.pages.home_page import HomePage
from libs.pages.settings_page import SettingsPage
from libs.pages.chart_page import ChartPage
from libs.pages.base_page import BasePage
from libs.pages.todo_page import TodoPage

# DATE

todaysDate = datetime.today().strftime("%Y-%m-%d")

# GIF

GIF = ft.Image(
        src="assets/icons/animegirly.gif",  
        width=64, 
        height=64,
        fit=ft.ImageFit.CONTAIN  
    )

# CONFIG

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "folder_path": "/logs",
    "color": "1",
    "AI": "",
    "prompt": ""
}

def save_config(config_data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file, indent=4)

def load_config():
    try:
        if not os.path.exists(CONFIG_FILE):
            save_config(DEFAULT_CONFIG)
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return DEFAULT_CONFIG
    
config = load_config()
folder_path = config.get("folder_path")

# LOGS

def load_log(file):
    try:
        with open(f"{folder_path}\\{file}", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)


# REACTIVE TIME

def get_time_based_color():
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return "#7DAA6A"  
        elif 12 <= hour < 18:
            return "#D69465"   
        else:
            return "#907bd2"
        
# PAGE SETTINGS

def show_page(page_name, page: ft.Page):
    page.controls.clear()

    if page_name == "home":
        page.add(HomePage(page))
    elif page_name == "settings_page":
        page.add(SettingsPage(page))
    elif page_name == "base_page":
        page.add(BasePage(page))
    elif page_name == "chart_page":
        page.add(ChartPage(page))
    elif page_name == "todo_page":
        page.add(TodoPage(page))

    page.update()

def theme_switch(e, page: ft.Page):
        selected_theme = e.control.content.value  
        if selected_theme == "SYSTEM":
            page.theme_mode = ft.ThemeMode.SYSTEM
        elif selected_theme == "DARK":
            page.theme_mode = ft.ThemeMode.DARK
        elif selected_theme == "LIGHT":
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()