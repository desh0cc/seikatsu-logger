import flet as ft, json, os
from datetime import datetime

# DATE

todaysDate = datetime.today().strftime("%Y-%m-%d")

# CONFIG

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "folder_path": "/logs",
    "language": "en_US",
    "model": ""
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
    

# LOGS

def load_log(file):
    config = load_config()
    folder_path = config.get("folder_path")
    try:
        with open(f"{folder_path}\\{file}", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)

# LANGUAGE LOADING

def lang_load(key):
    config = load_config()
    try:
        with open(f"lang/{config.get("language")}", "r", encoding="utf-8") as f:
            translations = json.load(f)
        return translations.get(key)
    except FileNotFoundError:
        print("Translations file not founded")


# REACTIVE TIME

def get_time_based_color():
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return "#A67B5B"  
        elif 12 <= hour < 18:
            return "#7DAA6A" 
        else:
            return "#907bd2"
        
# PAGE SETTINGS

def theme_switch(e, page: ft.Page):
        selected_theme = e.control.content.value  
        if selected_theme == "SYSTEM":
            page.theme_mode = ft.ThemeMode.SYSTEM
        elif selected_theme == "DARK":
            page.theme_mode = ft.ThemeMode.DARK
        elif selected_theme == "LIGHT":
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()