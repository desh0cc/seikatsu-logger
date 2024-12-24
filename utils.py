import json, os
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
    """Загрузка логів"""
    config = load_config()
    folder_path = config.get("folder_path")
    try:
        with open(f"{folder_path}\\logs\\{file}", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)

def if_intersect(new_start, new_end, existing_logs) -> bool:
    """Перевірка на стик часу логів"""
    new_start = datetime.strptime(new_start, "%H:%M:%S")
    new_end = datetime.strptime(new_end, "%H:%M:%S")
    
    for log_id, log in existing_logs.items():
        start_existing = datetime.strptime(log["start_time"], "%H:%M:%S")
        end_existing = datetime.strptime(log["end_time"], "%H:%M:%S")
        
        if new_start < end_existing and new_end > start_existing:
            return True

    return False

def duration_to_seconds(duration: str) -> str:
    """Перевод часу в секунди"""
    times = duration.split(":")
    return str((int(times[0]) * 3600) + (int(times[1]) * 60) + int(times[2]))
        
# LANGUAGE LOADING

def lang_load(key, **kwargs):
    config = load_config()
    try:
        lang_file = f"lang/{config.get('language')}"
        
        with open(lang_file, "r", encoding="utf-8") as f:
            translations = json.load(f)

        template = translations.get(key)
        if template is None:
            print(f"Key '{key}' not found in translations")
            return key

        return template.format(**kwargs)
    
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Translations file '{lang_file}' not found")
        return key


# REACTIVE TIME

def get_time_based_color():
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return "#A67B5B"  
        elif 12 <= hour < 18:
            return "#7DAA6A" 
        else:
            return "#907bd2"
        
if __name__ == "__main__":
    print(duration_to_seconds("03:25:30"))