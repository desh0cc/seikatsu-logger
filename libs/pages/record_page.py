import flet as ft, time, os, json, threading
from datetime import datetime, timedelta
from libs.components.NavigationComp import BackToHome

from utils import todaysDate, get_time_based_color, load_config, lang_load

def record_page(page: ft.Page) -> ft.View:    
    start_value = "0:00:00"
    record_label = ft.Text(value=start_value, size=35, font_family="Helvetica", weight=ft.FontWeight.BOLD)

    config = load_config()
    folder_path = config.get("folder_path")

    activity_input = ft.Text("")

    def start_recording():
        global stop_recording_flag, start_time
        stop_recording_flag = False  
        start_time = datetime.now()  
        print(start_time.strftime("%H:%M:%S"))

        def record_loop():
            global record_duration, stop_recording_flag, end_time
            record_duration = timedelta()
            while not stop_recording_flag:
                time.sleep(1)
                record_duration += timedelta(seconds=1)
                record_label.value = str(record_duration)
                page.update()  

            
            end_time = datetime.now()
            print(end_time.strftime("%H:%M:%S"))

        threading.Thread(target=record_loop).start()

    def stop_recording():
        global stop_recording_flag
        stop_recording_flag = True  
        record_label.value = str(record_duration)  
        page.update()

    def delete_recording():
        global record_duration 
        record_duration = timedelta() 
        record_label.value = start_value  
        page.update()

    def on_change_activity(e):
        activity_input.data = e.control.value
        page.update()

    def write_down(event, start_time, end_time, total_time):

        if not os.path.exists(f"{folder_path}/logs/"):
            os.makedirs(f"{folder_path}/logs/")

        try:
            with open(f"{folder_path}/logs/{todaysDate}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        start_time_str = start_time.strftime('%H:%M:%S') if start_time else "Not recorded"
        end_time_str = end_time.strftime('%H:%M:%S') if end_time else "Not recorded"

        data[event] = {
            "start_time": start_time_str,
            "end_time": end_time_str,
            "duration": str(total_time)
        }

        try:
            with open(f"{folder_path}/logs/{todaysDate}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            page.open(ft.SnackBar(ft.Text(lang_load(f"record_page_success_message", date=todaysDate)), bgcolor=ft.Colors.GREEN_ACCENT))
        except Exception as e:
            print(f"Error writing to file: {e}")
            page.open(ft.SnackBar(ft.Text(lang_load("record_page_error_message")), bgcolor=ft.Colors.RED_ACCENT))
            
    navigator = BackToHome(lang_load("record_page_title"), page)

    content = ft.Column([
        navigator.add(),
        
        ft.Container(
            content=record_label,
            alignment=ft.alignment.top_center
        ),

        ft.Row([
            ft.Container(
                content=ft.IconButton(
                    icon_color=ft.Colors.GREEN_ACCENT,
                    icon=ft.Icons.PLAY_CIRCLE,
                    width=45,
                    height=45,
                    on_click=lambda e: start_recording()
                )
            ),
            ft.Container(
                content=ft.IconButton(
                    icon_color=ft.Colors.YELLOW_ACCENT,
                    icon=ft.Icons.STOP_CIRCLE,
                    width=45,
                    height=45,
                    on_click=lambda e: stop_recording()
                )
            ),
            ft.Container(
                content=ft.IconButton(
                    icon_color=ft.Colors.RED_ACCENT,
                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                    width=45,
                    height=45,
                    on_click=lambda e: delete_recording()
                )
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Container(
            ft.Column([
                ft.Container(
                    ft.Text(lang_load("record_page_activity_title"), size=16), 
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    ft.TextField(
                        width=200,
                        text_align=ft.TextAlign.LEFT,
                        color=ft.Colors.WHITE,
                        border_color=get_time_based_color(),
                        label_style=ft.TextStyle(color=get_time_based_color()),
                        on_change=on_change_activity
                    ), alignment=ft.alignment.center
                ),
                activity_input
            ])
        ),

        ft.Container(
            content=ft.ElevatedButton(
                text=lang_load("record_page_save_button"),
                color=get_time_based_color(),
                on_click=lambda e: write_down(activity_input.data, start_time, end_time, record_label.value)
            ),
            alignment=ft.alignment.center
        )
    ])
    return ft.Column([content], expand=True)