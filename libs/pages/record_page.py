import flet as ft, time, os, json, threading
from datetime import datetime, timedelta
from libs.components.Back import BackToHome

def record_page(page: ft.Page) -> ft.View:
    from utils import todaysDate, get_time_based_color, folder_path

    start_time = None 
    end_time = None

    record_duration = timedelta()
    
    start_value = "0:00:00"
    record_label = ft.Text(value=start_value, size=35, font_family="Helvetica", weight=ft.FontWeight.BOLD)

    activity_input = ft.Text("")

    def start_recording():
        stop_recording_flag = False  
        start_time = datetime.now()  
        print(start_time.strftime("%H:%M:%S"))

        def record_loop():
            while not stop_recording_flag:
                time.sleep(1)
                record_duration += timedelta(seconds=1)
                record_label.value = str(record_duration)
                page.update()  

            end_time = datetime.now()
            print(end_time.strftime("%H:%M:%S"))

        threading.Thread(target=record_loop).start()

    def stop_recording():
        stop_recording_flag = True  
        record_label.value = str(record_duration)  
        page.update()

    def delete_recording():
        record_duration = timedelta() 
        record_label.value = start_value  
        page.update()

    def on_change_activity(e):
        activity_input.data = e.control.value
        page.update()

    def write_down(event, start_time, end_time, total_time):
        try:
            with open(f"{todaysDate}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        file_path = os.path.join(folder_path, f"{todaysDate}.json")
        start_time_str = start_time.strftime('%H:%M:%S') if start_time else "Not recorded"
        end_time_str = end_time.strftime('%H:%M:%S') if end_time else "Not recorded"

        data[event] = {
            "start_time": start_time_str,
            "end_time": end_time_str,
            "duration": str(total_time)
        }

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            page.open(ft.SnackBar(ft.Text(f"Успішно занесено у {todaysDate}.json!"), bgcolor=ft.colors.GREEN_ACCENT))
        except Exception as e:
            print(f"Error writing to file: {e}")
            page.open(ft.SnackBar(ft.Text("Виникла проблема"), bgcolor=ft.colors.RED_ACCENT))
            
    navigator = BackToHome("Записати лог", page)

    content = ft.Column([
        navigator.add(),
        
        ft.Container(
            content=record_label,
            alignment=ft.alignment.top_center
        ),
        ft.Row([
            ft.Container(
                content=ft.IconButton(
                    icon_color=ft.colors.GREEN_ACCENT,
                    icon=ft.icons.PLAY_CIRCLE,
                    width=45,
                    height=45,
                    on_click=lambda e: start_recording()
                )
            ),
            ft.Container(
                content=ft.IconButton(
                    icon_color=ft.colors.YELLOW_ACCENT,
                    icon=ft.icons.STOP_CIRCLE,
                    width=45,
                    height=45,
                    on_click=lambda e: stop_recording()
                )
            ),
            ft.Container(
                content=ft.IconButton(
                    icon_color=ft.colors.RED_ACCENT,
                    icon=ft.icons.DELETE_OUTLINE_ROUNDED,
                    width=45,
                    height=45,
                    on_click=lambda e: delete_recording()
                )
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),


        ft.Container(
            ft.Column([
                ft.Container(
                    ft.Text("Назва активності:", size=16), 
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    ft.TextField(
                        width=200,
                        text_align=ft.TextAlign.LEFT,
                        label="Активність",
                        hint_text="Введіть назву активності",
                        color=ft.colors.WHITE,
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
                text="Додати",
                color=get_time_based_color(),
                on_click=lambda e: write_down(activity_input.data, start_time, end_time, record_label.value)
            ),
            alignment=ft.alignment.center
        )
    ])
    return ft.Column([content], expand=True)
